import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup WebDriver
driver = webdriver.Chrome()
driver.get("https://devpost.com/hackathons?challenge_type[]=online&order_by=deadline&status[]=upcoming&status[]=open")

# Wait until hackathons load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.hackathon-tile"))
)

# Manual scrolling instruction
print("\n[INFO] Manually scroll down to load all hackathons.")
print("[INFO] Press 'q' and hit Enter when done.\n")

while True:
    user_input = input("Press 'q' and hit Enter to proceed: ")
    if user_input.lower() == 'q':
        break

# Extract hackathons
hackathons = driver.find_elements(By.CSS_SELECTOR, "div.hackathon-tile")

# Date range filter
start_date_min = datetime.strptime("25/03/25", "%d/%m/%y")
start_date_max = datetime.strptime("30/04/25", "%d/%m/%y")

hackathon_list = []  # Store extracted data

for hackathon in hackathons:
    try:
        title = hackathon.find_element(By.CSS_SELECTOR, "h3").text
        hackathon_url = hackathon.find_element(By.CSS_SELECTOR, "a.tile-anchor").get_attribute("href")
        date_text = hackathon.find_element(By.CSS_SELECTOR, "div.submission-period").text

        # Try to find location (optional)
        try:
            location = hackathon.find_element(By.CSS_SELECTOR, "div.info-with-icon i.fa-map-marker-alt + div.info").text
        except:
            location = "online"

        # Try to find participants count (optional)
        try:
            participants = hackathon.find_element(By.CSS_SELECTOR, "div.participants strong").text
        except:
            participants = "N/A"

        # Try to find prize info (optional)
        try:
            prize_info = hackathon.find_element(By.CSS_SELECTOR, "div.prize").text
        except:
            prize_info = "N/A"

        # Try to find themes (optional)
        themes = [theme.text for theme in hackathon.find_elements(By.CSS_SELECTOR, "span.theme-label")] or ["N/A"]

        # Extract start date (first date in range)
        match = re.search(r"(\w+ \d{1,2}), (\d{4})", date_text)
        if match:
            start_date = datetime.strptime(f"{match.group(1)}, {match.group(2)}", "%b %d, %Y")

            # Check if start date is within range
            if start_date_min <= start_date <= start_date_max:
                hackathon_list.append((start_date, title, hackathon_url, date_text, location, participants, prize_info, themes))

    except Exception as e:
        print("Error extracting hackathon:", e)

# Sort hackathons by start date
hackathon_list.sort()

# Print sorted results
for start_date, title, hackathon_url, date_text, location, participants, prize_info, themes in hackathon_list:
    print(f"Title: {title}")
    print(f"URL: {hackathon_url}")
    print(f"Dates: {date_text}")
    print(f"Location: {location}")
    print(f"Participants: {participants}")
    print(f"Prizes: {prize_info}")
    print(f"Themes: {', '.join(themes)}")
    print("-" * 50)

# Close driver
driver.quit()
