# RI ENTERPRISES Online Services Website

A Flask website for **RI ENTERPRISES** (Founder: **RAFEEQ AHMED HUSSAIN**) to list online government-style services, show sample certificate images, and save customer details directly to an Excel file.

## Features

- Public service catalog with name and amount (₹)
- Sample certificate image per service
- Customer form: name, mobile (10 digits), Aadhaar (12 digits)
- Each submission saved to `data/records.xlsx`
- Password-protected admin panel to add, edit, and delete services
- Upload and replace sample certificate images

## Requirements

- Python 3.10 or newer
- Windows PC (or any OS with Python)

## Setup on Windows

### Easy way (recommended)

1. Double-click **`INSTALL.bat`** (first time only)
2. Double-click **`START_WEBSITE.bat`**
3. Your browser will open at http://127.0.0.1:5000

Keep the black window open while using the website. Close it to stop the server.

**Important:** Do not open HTML files directly from the folder. This site must run through Python/Flask.

### Manual way (PowerShell)

```powershell
cd "c:\Cursor\PY 1"
```

2. Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Create your environment file:

```powershell
copy .env.example .env
```

5. Edit `.env` and set your admin password:

```
SECRET_KEY=your-random-secret-key-here
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_password
```

6. Start the website:

```powershell
python app.py
```

7. Open in your browser:

- **Public site:** http://127.0.0.1:5000
- **Admin login:** http://127.0.0.1:5000/admin/login

Default admin username is `admin` (change in `.env`).

## How to Use

### For customers (public site)

1. Open the home page and click a service card.
2. View the sample certificate image.
3. Enter customer name, mobile number, and Aadhaar number.
4. Click **Save to Excel** — the record is added immediately.

### For admin (you)

1. Go to **Admin** and log in with your username and password.
2. Use **Manage Services** to:
   - Add new services with name, amount, and sample certificate image
   - Edit existing services or replace images
   - Delete services
3. Log out when finished.

## Excel File Location

Customer records are saved to:

```
c:\Cursor\PY 1\data\records.xlsx
```

Columns:

| Date & Time | Service Name | Amount | Customer Name | Mobile | Aadhaar |

Open this file in Microsoft Excel anytime to view all customer entries.

## Data & Security Notes

- **Aadhaar numbers are sensitive.** Keep the `data` folder on a secure PC with restricted access.
- Do not share your `.env` file or admin password.
- Uploaded certificate images are stored in `uploads/certificates/`.
- Service data is stored in `data/services.db` (SQLite).

## Project Structure

Built with **HTML + CSS + JavaScript** frontend and **Python Flask** backend.

```
templates/            HTML pages (Jinja2)
static/
  css/style.css       All website styling
  js/main.js          Navigation, flash messages, UI
  js/customer-form.js Form validation (mobile, Aadhaar)
  js/admin.js         Image preview, delete confirm
app.py                Main Flask application (Excel + admin API)
config.py             Settings and company info
database.py           SQLite service storage
excel_store.py        Excel read/write and validation
auth_utils.py         Admin login helpers and file upload
data/                 Database and Excel files (auto-created)
uploads/              Certificate images
```

## Troubleshooting

- **Website not opening:** Double-click `START_WEBSITE.bat` — do not open HTML files directly in the browser.
- **Python not found:** Install Python from https://www.python.org/downloads/ and check **"Add Python to PATH"** during install, then run `INSTALL.bat` again.
- **Port already in use:** Close any other black command windows running the website, then start again.
- **Excel file locked:** Close Excel if `records.xlsx` is open, then submit the form again.
- **Cannot log in:** Check `ADMIN_USERNAME` and `ADMIN_PASSWORD` in your `.env` file.

## Optional: Run on Your Local Network

To allow other devices on the same Wi-Fi to access the site, change `host` in `app.py` to `0.0.0.0` and use your PC's IP address instead of `127.0.0.1`. Only do this on a trusted network.
