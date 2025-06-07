
# User Creation Program

## Overview
This Python program is designed to process user data from a CSV file and create users via an API endpoint.


## Requirements
- Python 3.x
- `requests` library (installed via `requirements.txt`)

## Setup
1. Clone or download this project.
2. Ensure you have Python 3 installed.
3. Install the required dependencies using `pip`:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Program
1. Place your `users.csv` file inside the `users/` folder.
2. Add valid roles to `roles.txt` in the `roles/` folder.
3. Run the program:
   ```bash
   python User_create.py
   ```

## Error Logging
- All errors (invalid data, API issues, missing fields) are logged in the `logger/error_log.txt` file.
- The log will contain information about skipped rows, invalid fields, and API response errors.

## Common Errors
- **403 Forbidden**: Authentication or permission issues with the API. Ensure the correct **API key** or **token** is provided.
- **400 Bad Request**: Invalid data in the request. Ensure all fields (`name`, `email`, `role`) are valid and properly formatted.
- **404 Not Found**: The API endpoint might be incorrect. Verify the URL.


