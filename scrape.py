from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

# Scrapes the full HTML of a given website using Selenium
def scrape_website(website, headless=True, max_duration=30):
    print("Launching browser...")

    # Path to your local ChromeDriver executable
    chrome_driver_path = "./chromedriver.exe"

    # Configure Chrome browser options
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")       # Run browser invisibly (no UI)
        options.add_argument("--disable-gpu")    # Avoid GPU-related issues in headless mode

    # Launch the browser with specified options
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
    start_time = time.time()  # Track how long the page takes to load

    try:
        driver.get(website)  # Navigate to the target URL

        # Wait until the page is fully loaded or timeout is reached
        while time.time() - start_time < max_duration:
            if driver.execute_script("return document.readyState") == "complete":
                break
            time.sleep(1)  # Wait a bit before checking again

        #Final check: did we exceed timeout?
        if time.driverexecute_script("return document.readyState") 

            # Check if the page is fully loaded (document.readyState === "complete")
            if driver.execute_script("return document.readyState") == "complete":
                break

            time.sleep(5)  # Wait before checking again

        print(f"Successfully navigated to {website}")
        html = driver.page_source  # Capture the full HTML content
        return html

    finally:
        driver.quit()  # Always close the browser, even if an error occurs
        print("Browser closed.")

# Extracts the <body> tag from the full HTML
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

# Cleans the body content by removing scripts, styles, and excess whitespace
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove all <script> and <style> tags
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Optionally preserve <h2>, <section>, etc.
    for tag in soup.find_all(["h1", "h2", "h3", "section", "article", "nav", "footer", "header"]):  
        tag.insert_before("\n===SECTION BREAK==\n")

    # Extract readable text with line breaks
    cleaned_content = soup.get_text(separator="\n")
    # Strip extra whitespace and empty lines
    cleaned_content = "\n".join(line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

# Splits long DOM content into manageable chunks (e.g., for AI parsing)
def split_dom_content(dom_content, marker="===SECTION BREAK==="):
    return [chunk.strip() for chunk in dom_content.split(marker) if chunk.strip()]
