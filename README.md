# ScrapperWithCookies

A simple Web Scrapper with Cookies and Headers. Just for a demonstration for a project.

## Description

`WebScraperConCookies` is a Python-based web scraping utility that handles cookies and maintains session persistence across multiple HTTP requests. It's designed to simulate realistic browser behavior by managing cookies automatically and using authentic headers.

## Features

- **Automatic Cookie Management**: Maintains cookies across requests using `requests.Session()`
- **Cookie Persistence**: Load and save cookies from/to Netscape/Mozilla format files
- **Manual Cookie Injection**: Add custom cookies programmatically
- **Realistic Headers**: Includes browser-like User-Agent and headers to avoid blocking
- **GET & POST Support**: Perform both GET and POST requests while maintaining session state
- **BeautifulSoup Integration**: Parse HTML content easily with built-in example

## Requirements

```bash
pip install requests beautifulsoup4
```

## Usage

### Basic Example

```python
from web_scraper import WebScraperConCookies

# Initialize scraper with optional cookie file
scraper = WebScraperConCookies(cookies_file="my_cookies.txt")

# Perform GET request
response = scraper.get("https://example.com")

# Parse HTML content
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.title.string)
```

### Working with Cookies

```python
# Load cookies from file (automatic if file exists)
scraper.cargar_cookies()

# Add cookies manually
scraper.agregar_cookies_manual({
    "session_id": "abc123",
    "user_token": "xyz789"
})

# Save current cookies to file
scraper.guardar_cookies()
```

### Making Requests

```python
# GET request
response = scraper.get("https://example.com", params={"page": 1})

# POST request
response = scraper.post("https://example.com/login", 
                       data={"username": "user", "password": "pass"})
```

## Demo Script

Run the included demo to see the scraper in action:

```bash
python web_scraper.py
```

The demo demonstrates:
1. Setting cookies via GET request
2. Verifying cookie persistence
3. Saving cookies to file
4. Adding manual cookies
5. Scraping real website content (Python España)

## Cookie File Format

Cookies are saved in Netscape/Mozilla format (`.txt`), which is compatible with many browsers and tools.

## Notes

- This is a **demonstration project** for educational purposes
- Always respect `robots.txt` and website terms of service
- Use responsibly and ethically when scraping websites
- Some websites may block automated requests despite realistic headers
