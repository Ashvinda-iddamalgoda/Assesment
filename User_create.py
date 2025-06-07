import csv
import requests
import logging
import os

# API endpoint
API_ENDPOINT = "https://example.com/api/create_user"  # Replace with actual API endpoint

# File Paths and verifying
MAIN_DIR = "/Users/pasinduashvin/Downloads/Assessment"
CSV_FILE_PATH = os.path.join(MAIN_DIR, "users", "users.csv")  
LOG_FILE_PATH = os.path.join(MAIN_DIR, "log", "error_log.txt")
ROLES_FILE_PATH = os.path.join(MAIN_DIR, "roles", "roles.txt")  

# Ensure folders exist in the system
os.makedirs(os.path.join(MAIN_DIR, "log"), exist_ok=True)
os.makedirs(os.path.join(MAIN_DIR, "roles"), exist_ok=True) 
os.makedirs(os.path.join(MAIN_DIR, "users"), exist_ok=True)  

#S et up logger
logging.basicConfig(filename=LOG_FILE_PATH, level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load roles file
def load_roles():
    try:
        with open(ROLES_FILE_PATH, 'r') as f:
            return {line.strip() for line in f if line.strip()}
    except FileNotFoundError:
        logging.error(f"Roles file '{ROLES_FILE_PATH}' not found.")
        return set()

# Validate user data (check  name, email, and role are present and valid)
def is_valid_user(row, valid_roles):
    name = row.get("name")
    email = row.get("email")
    role = row.get("role")
    
    # Check if required fields (name, email, role) are missing
    if not name:
        logging.error(f"Missing name in row: {row}")
    if not email:
        logging.error(f"Missing email in row: {row}")
    if not role:
        logging.error(f"Missing role in row: {row}")
    
    # Validate email (contains "@" and ".")
    if email and ("@" not in email or "." not in email):
        logging.error(f"Invalid email format in row: {row}")  # Log invalid email format
    
    # Check if role is in valid roles
    if role and role not in valid_roles:
        logging.error(f"Invalid role in row: {row}")  # Log invalid role

    return name and email and "@" in email and "." in email and role in valid_roles

# Create user through API call
def create_user(user_data):
    try:
        response = requests.post(API_ENDPOINT, json=user_data)
        if response.status_code != 201:
            logging.error(f"Failed to create user {user_data.get('name')} - Status {response.status_code}")  # Failed Creation logging
    except Exception as e:
        logging.error(f"Error creating user {user_data.get('name')}: {e}")

# Process CSV, validate and create users
def process_csv(file_path, valid_roles):
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not is_valid_user(row, valid_roles):
                    logging.error(f"Skipping invalid user data: {row}")
                    continue
                create_user(row)

    except FileNotFoundError:
        logging.error(f"CSV file '{file_path}' not found.")
    except Exception as e:
        logging.error(f"Error reading CSV: {e}")


# Main program
if __name__ == "__main__": 
    valid_roles = load_roles()
    
    if valid_roles:
        process_csv(CSV_FILE_PATH, valid_roles) 

        if os.path.getsize(LOG_FILE_PATH) > 0:
            print(f"Errors were logged to: {LOG_FILE_PATH}")
        else:
            print("Successfully Created Users")
    else:
        print("No valid roles found. Exiting.")  # Roles don't match
