import os
from dotenv import load_dotenv
import sys

print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")

print("Attempting to load .env file...")
load_dotenv()
print("Finished load_dotenv() call")

api_key = os.getenv('COINGECKO_API_KEY')
print(f"API Key: {api_key}")

print("All environment variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

print("\nContents of .env file:")
try:
    with open('.env', 'r') as f:
        print(f.read())
except FileNotFoundError:
    print(".env file not found in the current directory.")
except Exception as e:
    print(f"Error reading .env file: {e}")






