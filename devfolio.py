import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome WebDriver
driver = webdriver.Chrome()
driver.get("https://devfolio.co/hackathons/open")

# Wait for hackathon cards to load
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "div.CompactHackathonCard__StyledCard-sc-9ff45231-0"))
)

# Manual scrolling instruction
print("\n[INFO] Manually scroll down to load all hackathons.")
print("[INFO] Press 'q' and hit Enter when done.\n")

while True:
    user_input = input("Press 'q' and hit Enter to proceed: ")
    if user_input.lower() == 'q':
        break

# Extract all hackathons
hackathons = driver.find_elements(By.CSS_SELECTOR, "div.CompactHackathonCard__StyledCard-sc-9ff45231-0")

# Define date range filter
start_date_min = datetime.strptime("25/03/25", "%d/%m/%y")
start_date_max = datetime.strptime("30/04/25", "%d/%m/%y")

hackathon_list = []  # Store extracted data

for index, hackathon in enumerate(hackathons):
    try:
        print(f"\n[INFO] Extracting hackathon {index + 1}...")

        # Title
        title = hackathon.find_element(By.CSS_SELECTOR, "h3").text

        # Hackathon URL
        hackathon_url = hackathon.find_element(By.CSS_SELECTOR, "a.Link__LinkBase-sc-e5d23d99-0").get_attribute("href")

        # Type of event (e.g., Hackathon)
        event_type = hackathon.find_element(By.CSS_SELECTOR, "p.sc-dkzDqf.jrEOye").text

        # Theme (if available)
        try:
            theme = hackathon.find_element(By.CSS_SELECTOR, "div.bZSCpz p.sc-dkzDqf").text
        except:
            theme = "Not specified"

        # Social media link (e.g., Instagram)
        try:
            social_media = hackathon.find_element(By.CSS_SELECTOR, "a.PillButton-sc-7655a019-0").get_attribute("href")
        except:
            social_media = "Not available"

        # Number of participants
        try:
            participants = hackathon.find_element(By.CSS_SELECTOR, "p.sc-dkzDqf.hDculK").text
        except:
            participants = "Not specified"

        # Mode of event (Online/Offline)
        try:
            mode = hackathon.find_elements(By.CSS_SELECTOR, "div.CCkVy p.sc-dkzDqf.cqgLqK")[0].text
        except:
            mode = "Not specified"

        # Status (e.g., Open, Closed)
        try:
            status = hackathon.find_elements(By.CSS_SELECTOR, "div.CCkVy p.sc-dkzDqf.cqgLqK")[1].text
        except:
            status = "Not specified"

        # Extract Start Date
        start_date_text = "Unknown"
        start_date = None
        for element in hackathon.find_elements(By.CSS_SELECTOR, "p.sc-dkzDqf.cqgLqK"):
            text = element.text
            match = re.search(r"(\d{2}/\d{2}/\d{2})", text)
            if match:
                start_date_text = match.group(1)
                start_date = datetime.strptime(start_date_text, "%d/%m/%y")
                break

        # Debugging output
        print(f"Title: {title}")
        print(f"Start Date: {start_date_text}")
        print(f"URL: {hackathon_url}")

        # Only add hackathons within date range
        if start_date and start_date_min <= start_date <= start_date_max:
            hackathon_list.append((
                start_date, title, hackathon_url, event_type, theme,
                social_media, participants, mode, status, start_date_text
            ))

    except Exception as e:
        print(f"[ERROR] Failed to extract hackathon {index + 1}: {e}")

# Sort hackathons by start date
hackathon_list.sort()

# Print sorted results
print("\n[INFO] Filtered Hackathons:")
for start_date, title, hackathon_url, event_type, theme, social_media, participants, mode, status, start_date_text in hackathon_list:
    print(f"\nTitle: {title}")
    print(f"URL: {hackathon_url}")
    print(f"Type: {event_type}")
    print(f"Theme: {theme}")
    print(f"Social Media: {social_media}")
    print(f"Participants: {participants}")
    print(f"Mode: {mode}")
    print(f"Status: {status}")
    print(f"Start Date: {start_date_text}")
    print("-" * 50)

# Close driver
driver.quit()
