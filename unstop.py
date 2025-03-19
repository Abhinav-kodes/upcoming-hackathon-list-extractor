import time
import re
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_days_left(text):
    """Extracts the number of days left from the given text."""
    match = re.search(r'(\d+)\s+days?', text)
    return int(match.group(1)) if match else None

def remove_overlay():
    """Continuously removes overlay elements in the background."""
    while True:
        try:
            overlays = driver.find_elements(By.CLASS_NAME, "cdk-overlay-container")
            for overlay in overlays:
                driver.execute_script("arguments[0].remove();", overlay)
            time.sleep(2)  # Adjust interval as needed
        except Exception as e:
            pass  # Prevents crashing due to minor errors

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize WebDriver
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://unstop.com/hackathons")

# Start overlay removal thread
overlay_thread = threading.Thread(target=remove_overlay, daemon=True)
overlay_thread.start()

# Increase timeout to 20 seconds
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cursor-pointer.single_profile"))
    )
except Exception as e:
    print("[ERROR] Hackathon elements not found. Try increasing timeout or checking CSS selector.")
    input("[INFO] Press Enter to exit...")
    driver.quit()
    exit()

# Prompt user for manual scrolling
print("\n[INFO] Scroll down manually to load more hackathons.")
input("[INFO] Press Enter when done scrolling...")

# Extract hackathons
hackathons = driver.find_elements(By.CSS_SELECTOR, "div.cursor-pointer.single_profile")

if not hackathons:
    print("[ERROR] No hackathons found. Check the website structure.")
    input("[INFO] Press Enter to exit...")
    driver.quit()
    exit()

data = []
for index, hackathon in enumerate(hackathons, start=1):
    try:
        title = hackathon.find_element(By.CSS_SELECTOR, "h2.double-wrap").text
        organization = hackathon.find_element(By.TAG_NAME, "p").text

        # Extract prize (if available)
        prize_element = hackathon.find_elements(By.CSS_SELECTOR, "div.seperate_box.align-center.prize")
        prize = prize_element[0].text if prize_element else "N/A"

        # Extract and parse deadline
        deadline_element = hackathon.find_elements(By.CSS_SELECTOR, "div.seperate_box.align-center.ng-star-inserted")
        deadline_text = deadline_element[-1].text if deadline_element else "N/A"
        days_left = extract_days_left(deadline_text)

        # ✅ Ensure filtering of hackathons between 7 and 50 days
        if days_left is not None:
            if 7 <= days_left <= 50:
                data.append({
                    "Title": title,
                    "Organization": organization,
                    "Prize": prize,
                    "Days Left": days_left,
                })
                
                # Debugging Info (Only for filtered hackathons)
                print(f"\n✅ Hackathon {index}:")
                print(f"🎯 Title: {title}")
                print(f"🏢 Organization: {organization}")
                print(f"💰 Prize: {prize}")
                print(f"⏳ Days Left: {days_left}")
                print("-" * 50)
            

    except Exception as e:
        print(f"[WARNING] Skipping a hackathon due to error: {e}")

# Print extracted hackathons
if data:
    print("\n[INFO] Filtered Hackathons:")
    for item in data:
        print(f"\nTitle: {item['Title']}")
        print(f"Organization: {item['Organization']}")
        print(f"Prize: {item['Prize']}")
        print(f"Days Left: {item['Days Left']}")
        print("-" * 50)
else:
    print("\n[INFO] No hackathons found within the given date range.")

# Keep browser open until user presses 'q'
print("\n[INFO] Type 'q' and press Enter in the terminal to close the browser.")

while True:
    user_input = input().strip().lower()
    if user_input == "q":
        print("[INFO] Closing browser...")
        driver.quit()
        break
    else:
        print("[INFO] Invalid input. Type 'q' and press Enter to exit.")
