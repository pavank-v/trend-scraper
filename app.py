from flask import Flask, render_template, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import uuid
import pymongo
import requests
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["trending_db"]
collection = db["trends"]

# Read proxies from file (set up proxies.txt using proxymesh proxies)
proxies = []
with open("proxies.txt", "r") as f:
    proxy = f.read().split('\n')
    for p in proxy:
        proxies.append(p)

# Function to fetch the current public IP address
def get_ip():
    try:
        ip = requests.get('https://api.ipify.org').text  # Using ipify to get current public IP
        return ip
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return "N/A"

# Function to create driver with a random proxy
def create_driver_with_proxy():
    proxy = random.choice(proxies)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument(f"--proxy-server=http://{proxy}")
    driver = webdriver.Chrome()
    driver.set_window_size(1600, 1000)
    return driver

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_script', methods=['POST'])
def run_script():
    driver = create_driver_with_proxy()
    driver.get("https://x.com/login/")

    email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    )
    email.click()
    email.send_keys(os.environ.get("TWITTER_USER_ID"))

    next_button = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '''//button[.//span[contains(text(), 'Next')]]'''))
    )
    next_button.click()

    password = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password.click()
    password.send_keys(os.environ.get("TWITTER_PASSWORD"))

    log = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//button[.//span[contains(text(), 'Log in')]]"))
    )
    log.click()

    explore_for_you = WebDriverWait(driver, 50).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/explore/tabs/for-you']//span[contains(text(), 'Show more')]"))
    )

    explore_for_you.click()

    arr = []
    for i in range(1, 5+1):
        trend = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.XPATH, f'''(//div[contains(@class, 'css-175oi2r r-16y2uox r-bnwqim')])[{i}]'''))
        )
        arr.append(trend.text)

    trends = []
    for tr in arr:
        if '\n' not in tr:
            trends.append(tr)
        else:
            trends.append(tr.split('\n')[1])

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip_address = get_ip()
    unique_id = str(uuid.uuid4())

    data = {
        "_id": unique_id,
        "trend1": trends[0] if len(trends) > 0 else None,
        "trend2": trends[1] if len(trends) > 1 else None,
        "trend3": trends[2] if len(trends) > 2 else None,
        "trend4": trends[3] if len(trends) > 3 else None,
        "trend5": trends[4] if len(trends) > 4 else None,
        "date_time": end_time,
        "ip_address": ip_address
    }
    collection.insert_one(data)

    driver.quit()

    # Returning the results in JSON format
    response_data = {
        'trends': trends,
        'ip_address': ip_address,
        'end_time': end_time,
        'unique_id': unique_id,
        'mongodb_entry': data
    }

    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)
