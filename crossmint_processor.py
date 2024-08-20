import logging
import requests # type: ignore
import time

logging.basicConfig(level=logging.INFO)


class CrossmintAPI:
    def __init__(self, candidate_id, rate_limit=1,max_retries=3):
        self.candidate_id = candidate_id
        self.base_url = "https://challenge.crossmint.io/api"
        self.rate_limit = rate_limit
        self.max_retries = max_retries
        self.last_request_time = 0

    def get_map(self):
        api_url = f"{self.base_url}/map/{self.candidate_id}/goal"
        response = self._rate_limited_request(requests.get, api_url)
        # print(response.json())
        return response.json()['goal']

    def post_polyanets(self, row, col):
        self._post_request("polyanets", {"row": row, "column": col})

    def post_soloons(self, row, col, color):
        # print((f"Posting Soloon at ({row}, {col}) with color {color}"))
        self._post_request("soloons", {"row": row, "column": col, "color": color})

    def post_comeths(self, row, col, direction):
        # print(f"Posting Cometh at ({row}, {col}) with direction {direction}")
        self._post_request("comeths", {"row": row, "column": col, "direction": direction})

    def _post_request(self, endpoint, data):
        api_url = f"{self.base_url}/{endpoint}"
        data["candidateId"] = self.candidate_id
        headers = {"Content-Type": "application/json"}
        # print("Posting data to", api_url, "with payload:", data)
        self._rate_limited_request(requests.post, api_url, json=data, headers=headers)

    def _rate_limited_request(self, request_func, *args, **kwargs):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < 1 / self.rate_limit:
            time.sleep((1 / self.rate_limit) - time_since_last_request)
        self.last_request_time = time.time()

        retries = 0
        while retries < self.max_retries:
            response = request_func(*args, **kwargs)
            if response.status_code == 429:  # Too Many Requests
                logging.warning(f"Rate limit exceeded. Waiting for 5 seconds.")
                time.sleep(5)
                continue
            if response.status_code == 500: # Internal Server Error
                logging.error(f"Server error. Retrying {retries + 1}/{self.max_retries} after delay.")
                time.sleep(2 ** retries)
                retries += 1
                continue
            if not response.ok:
                logging.error(f"Request failed with status code {response.status_code}: {response.text}")
                response.raise_for_status()
            return response
        
        logging.error(f"Max retries reached. Last request failed with status code {response.status_code}")
        response.raise_for_status()


class CellProcessor:
    def __init__(self, api):
        self.api = api

    def process_cell(self, i, j, cell_value):
        if cell_value == "SPACE":
            return
        string = cell_value.lower()
        if string == "polyanet":
            self.api.post_polyanets(i, j)
        else:
            string = string.split("_")
            param, obj = string[0], string[-1]
            if obj == "soloon":
                self.api.post_soloons(i, j, param)
            elif obj == "cometh":
                self.api.post_comeths(i, j, param)

    def process_map(self, matrix):
        total_cells = len(matrix) * len(matrix[0])
        processed_cells = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                self.process_cell(i, j, matrix[i][j])
                processed_cells += 1
                # Log progress every 50 cells processed
                if processed_cells % 50 == 0:
                    logging.info(f"Processed {processed_cells}/{total_cells} cells")


def main():
    candidate_id = "f2efd018-e451-4757-bcf1-0d4cbdc673df"
    api = CrossmintAPI(candidate_id)
    processor = CellProcessor(api)
    matrix = api.get_map()
    if matrix:
        processor.process_map(matrix)
    else:
        logging.error("Failed to retrieve the map data.")


if __name__ == "__main__":
    main()