# URL Shortener

A lightweight and fast URL Shortener API built using **Flask**, which generates **6-character alphanumeric short codes**, supports **analytics**, and handles **concurrent access** using in-memory storage.

---

## Features

- Shorten long URLs to a 6-character alphanumeric code
- Redirect to original URL using the short code
- Track number of times each URL is accessed
- Validates input URLs before shortening
- In-memory store (no external DBs required)
- Handles concurrent requests safely
- Fully tested using Pytest

---

## Tech Stack

- **Backend**: Python, Flask
- **Testing**: Pytest
- **Tools**: threading, concurrent.futures

---

## API Endpoints

### 1. Shorten URL  
**POST** `/api/shorten`  
```json
Request:
{
  "url": "https://example.com/long/article"
}

Response:
{
  "short_code": "abc123",
  "short_url": "http://localhost:5000/abc123"
}


### 2. Redirect to Origina
**GET** /<short_code>
- Redirects to the original URL if found
- Returns 404 if short code is invalid

### 3. URL Analytics
**GET** `/api/stats/<short_code>`  
```json
Response:
{
  "url": "https://example.com/long/article",
  "clicks": 12,
  "created_at": "2025-07-24T10:30:00"
}


### Installation
```bash
# Clone/download this repository
# Navigate to the assignment directory
cd Url Shortener

# Install dependencies
pip install -r requirements.txt

# Start the application
python -m flask --app app.main run

# The API will be available at http://localhost:5000
# Run tests with: pytest
```

<h3 align="center">
Thank You ❤️
</h3>