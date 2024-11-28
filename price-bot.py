import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pymysql

# Database Configuration
DB_HOST = "YOUR_DB_HOST"
DB_USER = "YOUR_DB_USER"
DB_PASSWORD = "YOUR_DB_PASSWORD"
DB_NAME = "YOUR_DB_NAME"
TABLE_NAME = "YOUR_TABLE_NAME"

# Google Sheets Configuration
CREDENTIALS_FILE = "credentials.json"
FILE_ID = "YOUR_GOOGLE_SHEET_FILE_ID"
SHEET_NAME = "YOUR_SHEET_NAME"

# Connect to Google Sheets
def fetch_google_sheet_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)

        # Open the specific spreadsheet by file ID
        sheet = client.open_by_key(FILE_ID).worksheet(SHEET_NAME)
        print(f"Opened Worksheet: {SHEET_NAME}")

        # Fetch all values
        data = sheet.get_all_values()
        return data
    except Exception as e:
        raise RuntimeError(f"Error fetching Google Sheets data: {e}")

def parse_and_store_data(sheet_data):
    print("Parsing Sheet Data...")
    connection = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = connection.cursor()

    # Clear existing data
    cursor.execute(f"TRUNCATE TABLE {TABLE_NAME}")

    ticker = None
    blank_row_count = 0

    for i, row in enumerate(sheet_data[2:], start=3):  # Start at the 3rd row
        if not row[1].strip():  # Skip rows without a ticker in column B
            blank_row_count += 1
            if blank_row_count == 2:
                print("Two consecutive blank rows detected. Ending parsing.")
                break
            continue
        blank_row_count = 0

        ticker = row[1].strip()  # Get the ticker from column B
        if not ticker:
            continue

        locations = row[3:]  # Starting from column D (index 3)
        prices = sheet_data[i][3:]  # Prices are in the same row, starting at column D

        for location, price in zip(locations, prices):
            location = location.strip()
            price = price.strip()

            if not location or not price:  # Skip empty locations or prices
                continue

            try:
                price = float(price)  # Convert price to a float
            except ValueError:
                print(f"Invalid price format at row {i}: {price}")
                continue

            # Insert data into the database
            cursor.execute(
                f"INSERT INTO {TABLE_NAME} (mat, location, price) VALUES (%s, %s, %s)",
                (ticker, location, price)
            )

    connection.commit()
    cursor.close()
    connection.close()
    print(f"Parsing complete. Last ticker processed: {ticker}")

# Main Function
if __name__ == "__main__":
    try:
        # Fetch data from Google Sheets
        sheet_data = fetch_google_sheet_data()

        # Parse and store the data
        parse_and_store_data(sheet_data)

        print("Database updated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
