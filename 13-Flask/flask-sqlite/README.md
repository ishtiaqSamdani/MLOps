# Flask Email List POC with SQLite

A simple proof-of-concept Flask application with SQLite for managing an email subscription list.

## Features

- ✅ Email subscription form at `/` (uses Jinja templating)
- ✅ Email validation (proper format check)
- ✅ SQLite database for data persistence
- ✅ Admin panel at `/admin` showing all subscribers in a table (uses Jinja templating)
- ✅ Delete functionality for each subscriber
- ✅ Dark mode UI with minimal CSS
- ✅ Separate REST APIs for GET and DELETE operations (optional)
- ✅ Server-side rendering with Jinja templates (no JavaScript required)

## Project Structure

```
flask-sqlite/
├── app.py                    # Main Flask application
├── templates/
│   ├── index.html           # Subscription form page
│   └── admin.html           # Admin panel with table
├── emaillist.db             # SQLite database (auto-created)
└── README.md                # This file
```

## Installation

1. Make sure you have Python 3 and Flask installed:
   ```bash
   pip install flask
   ```

2. Navigate to the flask-sqlite directory:
   ```bash
   cd flask-sqlite
   ```

3. Run the application:
   ```bash
   python3 app.py
   ```

4. Open your browser and visit:
   - `http://127.0.0.1:5000/` - Subscription form
   - `http://127.0.0.1:5000/admin` - Admin panel

## API Endpoints

### 1. Subscribe (POST)
- **URL**: `/api/subscribe`
- **Method**: POST
- **Form Data**: `name`, `email`
- **Response**: JSON with success/error message

### 2. Get All Subscribers (GET)
- **URL**: `/api/subscribers`
- **Method**: GET
- **Response**: JSON array of all subscribers

### 3. Delete Subscriber (DELETE)
- **URL**: `/api/subscribers/<id>`
- **Method**: DELETE
- **Response**: JSON with success/error message

## Usage

### Subscribing
1. Go to `http://127.0.0.1:5000/`
2. Enter your name and email
3. Click "Subscribe"
4. Page refreshes with success or error message

### Managing Subscribers (Admin)
1. Go to `http://127.0.0.1:5000/admin`
2. View all subscribers in a table (rendered with Jinja templating)
3. Click "Delete" button to remove a subscriber
4. Page refreshes to show updated list

## Email Validation

The application validates email addresses using regex pattern:
- Must have format: `username@domain.extension`
- Allows alphanumeric characters, dots, underscores, and hyphens
- Domain must have at least 2 characters in extension

## Dark Mode

The entire application uses a dark color scheme:
- Background: `#1a1a1a`
- Cards/Tables: `#2a2a2a`
- Text: `#e0e0e0`
- Primary color: `#4a9eff`

No light mode toggle - dark mode only as requested!

## Database Schema

```sql
CREATE TABLE email_list (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Notes

- The database file `emaillist.db` is created automatically on first run
- Email addresses must be unique (duplicate emails are rejected)
- Delete operations are confirmed with a JavaScript alert before submission
- **Both pages use Jinja templating** for server-side rendering (traditional Flask approach)
- **No JavaScript required** for core functionality (only for delete confirmation)
- Page refreshes after form submissions to show updated data
- REST API endpoints are still available but not used by the templates

