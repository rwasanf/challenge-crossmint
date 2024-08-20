

# Crossmint Metaverse Challenge

This script automates interactions with the Crossmint API to manage celestial objects. It retrieves a goal map and posts Polyanets, Soloons, and Comeths at specified positions.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rwasanf/challenge-crossmint.git
   cd challenge-crossmint
   ```

2. **Install Required Packages**:
   Install the necessary Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```
   If there is no \`requirements.txt\`, manually install the required library:
   ```bash
   pip install requests
   ```

## Usage

1. **Set Up the Candidate ID**:
   - Open the script (\`crossmint_processor.py\`) and update the \`candidate_id\` variable with your unique candidate ID.

2. **Run the Script**:
   To execute the script, run:
   ```bash
   python crossmint_processor.py
   ```
   This will start the process of retrieving the goal map and posting celestial objects based on the map's data.

## Configuration

- **API Base URL**:
  - The base URL for the Crossmint API is defined in the \`CrossmintAPI\` class. If the API changes or if you need to switch environments, you can update the \`BASE_URL\` in that class.
 
- **Rate Limiting**:
  - The script includes rate limiting to prevent overwhelming the Crossmint API. The `rate_limit` parameter in the `CrossmintAPI` class defines the maximum number of requests per second.
  - The `max_retries` parameter controls how many times the script will retry a request in case of errors like `429 Too Many Requests` or `500 Internal Server Error`.

- **Logging**:
  - The script uses Python's built-in `logging` module to log progress and errors. Logs are set to the `INFO` level by default, but you can adjust the logging level by modifying the `logging.basicConfig(level=logging.INFO)` line.

