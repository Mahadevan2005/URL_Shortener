# 🔗 URL Shortener

A lightweight and fast URL Shortener API built using **Flask**, which generates **6-character alphanumeric short codes**, supports **analytics**, and handles **concurrent access** using in-memory storage.

---

## 🚀 Features

- ✅ Shorten long URLs to a 6-character alphanumeric code
- 🔁 Redirect to original URL using the short code
- 📈 Track number of times each URL is accessed
- 🔐 Validates input URLs before shortening
- ⚡ In-memory store (no external DBs required)
- 🔄 Handles concurrent requests safely
- 🧪 Fully tested using Pytest

---

## 📦 Tech Stack

- **Backend**: Python, Flask
- **Testing**: Pytest
- **Tools**: threading, concurrent.futures

---

## ⚙️ API Endpoints

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
