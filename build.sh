#!/usr/bin/env bash
# exit on error
set -o errexit

# Install project dependencies
pip install -r requirements.txt

# Run the setup script to create/populate the DB only if it doesn't exist
# We use the same environment variable to find the correct path
DB_FILE_PATH="$ONRENDER_DISK_PATH/hospital_management.db"

if [ ! -f "$DB_FILE_PATH" ]; then
  echo "Database not found. Running setup script..."
  python setup_database.py # This script must also use the correct DB_FILE path!
else
  echo "Database already exists. Skipping setup."
fi