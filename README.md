# TrendScraper

## Description

This project is a web scraper that uses **Selenium** to gather the latest trending topics from **X.com (formerly Twitter)**. It leverages a proxy service to change IPs for each request to avoid being blocked. The results are stored in **MongoDB** and displayed on a simple **Flask** web page. The web page allows users to click a button, run the scraping script, and view the most happening topics along with the IP address used and the MongoDB record of the data.

---

## Table of Contents

1. [Technologies Used](#technologies-used)
2. [How It Works](#how-it-works)
3. [Prerequisites](#prerequisites)
4. [Installation Instructions](#installation-instructions)
5. [Usage](#usage)
6. [MongoDB Schema](#mongodb-schema)
7. [Screenshots](#screenshots)
8. [Contributing](#contributing)

---

## Technologies Used

- **Python**: For implementing the scraping script and Flask app.
- **Selenium**: For web scraping.
- **Flask**: For creating the web application.
- **MongoDB**: For storing the results.
- **Requests**: To fetch the public IP.
- **Proxies**: To change IP addresses during each request for anonymity and to avoid blocking.
- **UUID**: For generating unique IDs for each entry.

---

## How It Works

1. **Selenium** is used to navigate to the **X.com** login page and scrape the latest trending topics.
2. **Proxy rotation** ensures each request uses a different IP by selecting a random proxy from a list.
3. After scraping the data, it stores the trending topics and metadata like the IP address used and timestamp into **MongoDB**.
4. The **Flask** app serves a single page with a button. When clicked, it triggers the scraping process, retrieves the latest trends, and displays them along with the MongoDB record.

---

## Prerequisites

Before setting up the project, you need the following software:

- Python 3.x
- MongoDB running locally or remotely
- ChromeDriver (compatible with your version of Chrome)

Additionally, you'll need to install dependencies:

```bash
pip install selenium requests pymongo flask
```

## Installation Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/pavank-v/web-scrapper-selenium
    ```

2. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Start **MongoDB** on your local machine or connect to a remote instance.

4. Create a **proxies.txt** file in the root directory with the proxy list:
    ```makefile
    proxy1:port
    proxy2:port
    proxy3:port
    ```
5. Create **.env** file and add your X.com **username** and **password**
---
## Usage

1. **Running the Script**:

    * The Flask app serves a simple web page.
    * Clicking the button on the web page will trigger the Selenium scraper to fetch trending topics and store the data in MongoDB.

2. **Running the Flask App**:

    * To start the Flask server, run:
    
    ```bash
    python app.py
    ```

3. Open the web page in your browser at `http://127.0.0.1:5000`
---

## Mongodb Schema
- The MongoDB collection stores the scraped data in the following format:
```
{
  "_id": "unique_id",
  "trend1": "Name of trend1",
  "trend2": "Name of trend2",
  "trend3": "Name of trend3",
  "trend4": "Name of trend4",
  "trend5": "Name of trend5",
  "date_time": "Timestamp of when the script was run",
  "ip_address": "IP address used during the scrape"
}
```
## Screenshots
![Screenshot from 2025-01-03 17-25-01](https://github.com/user-attachments/assets/278519bc-7861-442a-a0e7-d66413a576a4)


## Contributing

If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request. Contributions are always welcome!

---
