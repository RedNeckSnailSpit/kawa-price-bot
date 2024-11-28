# Price-Bot

A Python script for parsing price data from Google Sheets and storing it in a MySQL database. Useful for managing price tracking in games or other systems.

---

## Features
- Connects to Google Sheets to fetch data.
- Parses rows based on specific logic:
  - Extracts material (ticker) from column B.
  - Extracts planet and price data starting from column D.
- Stores data in a MySQL database.

---

## Setup Instructions

Follow these steps to set up the project:

### 1. **Clone the Repository**
```bash
git clone https://github.com/YOUR_USERNAME/price-bot.git
cd price-bot
```

### 2. **Install Dependencies**
This script requires the following Python libraries:
- `gspread`: To interact with Google Sheets.
- `oauth2client`: To authenticate with the Google Sheets API.
- `pymysql`: To connect to the MySQL database.

Install them with:
```bash
pip install gspread oauth2client pymysql
```

### 3. **Create the `credentials.json` File**
To access Google Sheets, you need a service account and API credentials. Follow these steps:

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project or select an existing one.
3. Enable the **Google Sheets API** and the **Google Drive API** for the project.
4. Go to the **Credentials** section, click **Create Credentials**, and select **Service Account**.
5. Download the JSON key file and rename it to `credentials.json`.
6. Place the `credentials.json` file in the same directory as the script.

Make sure to share your Google Sheet with the service account email address (e.g., `your-service-account@your-project.iam.gserviceaccount.com`) with **Editor** permissions.

---

### 4. **Database Setup**
Create a MySQL database and a table for storing the data. Replace `YOUR_TABLE_NAME` with your desired table name:
```sql
CREATE DATABASE your_database_name;

USE your_database_name;

CREATE TABLE YOUR_TABLE_NAME (
    mat VARCHAR(255),
    location VARCHAR(255),
    price FLOAT
);
```

---

### 5. **Update Variables in `price-bot.py`**
Open `price-bot.py` and replace the following placeholder values with your actual details:

- **Database Configuration**
  ```python
  DB_HOST = "YOUR_DB_HOST"       # e.g., "localhost"
  DB_USER = "YOUR_DB_USER"       # e.g., "root"
  DB_PASSWORD = "YOUR_DB_PASSWORD"  # Your MySQL password
  DB_NAME = "YOUR_DB_NAME"       # e.g., "your_database_name"
  TABLE_NAME = "YOUR_TABLE_NAME" # e.g., "pricing"
  ```

- **Google Sheets Configuration**
  ```python
  CREDENTIALS_FILE = "credentials.json"
  FILE_ID = "YOUR_GOOGLE_SHEET_FILE_ID"   # The file ID of your Google Sheet
  SHEET_NAME = "YOUR_SHEET_NAME"          # The name of your worksheet
  ```

---

### 6. **Run the Script**
Execute the script to fetch data from the Google Sheet and store it in the database:
```bash
python price-bot.py
```

---

## Example Google Sheet Format

The script expects the Google Sheet to have the following format:
- **Row 1**: Headers (e.g., "Proxion", "Material", "Planet", ...)
- **Column B**: Material (Ticker)
- **Columns D onward**: Locations (e.g., planets) and prices.

Example:
| Proxion | Material   | Planet 1 | Planet 2 | Planet 3 |
|---------|------------|----------|----------|----------|
| 1234    | Material A | 10.5     | 12.0     | 9.8      |
| 5678    | Material B | 8.3      | 7.5      | 10.1     |

---

## Troubleshooting

1. **Authentication Errors:**
   Ensure your Google Sheet is shared with the service account email (found in `credentials.json`).

2. **Database Connection Errors:**
   Verify your MySQL server is running and the credentials are correct.

3. **Data Parsing Issues:**
   Ensure the Google Sheet follows the expected format (see the example above).

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Credits
See [CREDITS.md](CREDITS.md) for acknowledgments.
