# Twitter Scraper

A Python-based Twitter scraper that logs into Twitter (X), fetches trending topics, and stores the data in MongoDB. The scraper uses Selenium for web automation and BeautifulSoup for parsing.

The deployment was not successful due to a ChromeDriver error. However, the scraper functionality is working as expected.  
To demonstrate the scraper in action, please refer to the video below: 
[![Scraper demo](https://raw.githubusercontent.com/Harsha-10/Twitter-scrapper/blob/main/scrapper.mp4)]
## Features
- Automated Twitter login
- Fetch trending topics
- Store data in MongoDB
- Headless browsing with Selenium

## Prerequisites
- Python 3.7+
- MongoDB
- Google Chrome (Latest Version)
- Chromedriver (Compatible with Chrome version)

## Setup

### 1. Clone the Repository
```bash
$ git clone https://github.com/harsha-10/twitter-scraper.git
$ cd twitter-scraper
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
$ python -m venv venv
$ source venv/bin/activate  # For Windows: venv\Scripts\activate
```

### 3. Install Required Packages
```bash
$ pip install -r requirements.txt
```

### 4. Environment Variables
Create a `.env` file in the root directory with the following content:

```env
SCRAPERAPI_KEY=your_proxy_api_key
TWITTER_USERNAME=your_twitter_username
TWITTER_PASSWORD=your_twitter_password
TWITTER_PHONE=your_phone_or_email_if_asked
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority / https://localhost:27017
```

### 5. Install Chromedriver (Automatic Download)
```bash
$ pip install webdriver-manager
```

### 6. Ensure MongoDB is Running
```bash
$ mongod // If running locally
```

## Running the Scraper
```bash
$ python app.py
```

## Troubleshooting

### 1. Chromedriver Path Error
If you encounter errors related to `chromedriver` not found, update the code to auto-install:
```python
from webdriver_manager.chrome import ChromeDriverManager
CHROMEDRIVER_PATH = ChromeDriverManager().install()
```

### 2. MongoDB Connection Issues
Ensure MongoDB Atlas IP whitelisting allows connections from your machine or use:
```bash
0.0.0.0/0
```


