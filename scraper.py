import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv
import os

class TwitterScraper:
    def __init__(self):
        load_dotenv()
        self.PROXY_API = os.getenv("SCRAPERAPI_KEY")
        self.TWITTER_USERNAME = os.getenv("TWITTER_USERNAME")
        self.TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")
        self.TWITTER_PHONE = os.getenv("TWITTER_PHONE")
        self.MONGO_URI = os.getenv("MONGO_URI")
        client = MongoClient(self.MONGO_URI)
        self.db = client["twitter_scrapper"]
        self.collection = self.db["trending"]

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        CHROMEDRIVER_PATH = '/opt/render/project/chromedriver'
        service = Service(executable_path=CHROMEDRIVER_PATH)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def get_ip_address(self):
        try:
            response = requests.get("https://api64.ipify.org/?format=json")
            if response.status_code == 200:
                data = response.json()
                return data
        except Exception as e:
            print(f"Error fetching IP address: {e}")
            return None

    def login_to_twitter(self, retries=3):
        for attempt in range(retries):
            try:
                print(f"Login attempt {attempt + 1}...")
                self.driver.maximize_window()
                self.driver.get("https://x.com/login")
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.NAME, "text")))

                username_field = self.driver.find_element(By.NAME, "text")
                username_field.send_keys(self.TWITTER_USERNAME)
                username_field.send_keys(Keys.RETURN)
                try:
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.NAME, "text")))
                    email_input = self.driver.find_elements(By.NAME, "text")
                    if email_input:
                        email_input[0].send_keys(self.TWITTER_PHONE)
                        email_input[0].send_keys(Keys.RETURN)
                except TimeoutException:
                    pass

                WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.NAME, "password")))
                password_field = self.driver.find_element(By.NAME, "password")
                password_field.send_keys(self.TWITTER_PASSWORD)
                password_field.send_keys(Keys.RETURN)

                try:
                    WebDriverWait(self.driver, 2).until(EC.presence_of_element_located((By.NAME, "text")))
                    email_input = self.driver.find_elements(By.NAME, "text")
                    if email_input:
                        email_input[0].send_keys(self.TWITTER_PHONE)
                        email_input[0].send_keys(Keys.RETURN)
                except TimeoutException:
                    pass

                print("Login successful.")
                return True
            except Exception as e:
                print(f"Login failed on attempt {attempt + 1}: {e}")
                time.sleep(5)

        print("All login attempts failed.")
        return False

    def fetch_trending_topics(self, ip_address, retries=3):
        for attempt in range(retries):
            try:
                print(f"Fetching trending topics attempt {attempt + 1}...")
                self.driver.maximize_window()
                self.driver.get("https://x.com/home")

                WebDriverWait(self.driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Trending now']"))
                )

                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                trending_section = soup.find("div", {"aria-label": "Timeline: Trending now"})

                if not trending_section:
                    print("No trending topics found.")
                    continue

                trends = trending_section.find_all("div", {"data-testid": "trend"})
                trending_data = []

                for trend in trends[:5]:
                    try:
                        trend_element = trend.find("div")
                        span_elements = trend_element.find_all("div", recursive=False)[:3]
                        trend_info = {
                            "location": span_elements[0].get_text(strip=True),
                            "trend_name": span_elements[1].get_text(strip=True),
                            "posts": span_elements[2].get_text(strip=True),
                            "ip": ip_address,
                        }
                        trending_data.append(trend_info)
                    except Exception as e:
                        print(f"Error parsing trend: {e}")
                        continue

                if trending_data:
                    self.collection.insert_many(trending_data)
                    print("Trending topics saved to MongoDB.")
                    return trending_data
            except Exception as e:
                print(f"Failed to fetch trending topics on attempt {attempt + 1}: {e}")
                time.sleep(5)

        print("All attempts to fetch trending topics failed.")
        return None

    def run(self):
        try:
            ip_data = self.get_ip_address()
            if not ip_data:
                raise Exception("Failed to fetch IP address.")

            if not self.login_to_twitter():
                raise Exception("Login process failed after multiple attempts.")

            trending_topics = self.fetch_trending_topics(ip_data["ip"])
            if trending_topics:
                print("Fetched Trending Topics:")
                for trend in trending_topics:
                    print(f"Location: {trend['location']}, Trend Name: {trend['trend_name']}, Posts: {trend['posts']}")
            else:
                raise Exception("Failed to fetch trending topics after multiple attempts.")
            ans = True
        except Exception as e:
            print(f"An error occurred: {e}")
            ans = False
        finally:
            self.driver.quit()
            return ans

if __name__ == "__main__":
    scraper = TwitterScraper()
    scraper.run()
