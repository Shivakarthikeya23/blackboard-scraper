from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Blackboard URL
bb_url = "https://blackboard.cmich.edu/ultra/course"

# Login credentials
email = "ralla1s@cmich.edu"
global_id = "ralla1s"
password = "ShivaKarthik@2311"

# Open Blackboard
driver.get(bb_url)

try:
    # Step 1: Enter Email
    email_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "i0116")))
    email_field.send_keys(email)

    # Click Next
    next_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
    next_button.click()

    # Wait for Global ID & Password fields to be visible
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "field-1")))

    # Step 2: Enter Global ID
    global_id_field = driver.find_element(By.ID, "field-1")
    global_id_field.send_keys(global_id)

    # Step 3: Enter Password
    password_field = driver.find_element(By.ID, "field-2")
    password_field.send_keys(password)

    # Step 4: Click "Log In" button
    login_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "SubmitCreds")))
    login_button.click()

    # Handle Duo 2FA (Wait 10-15 seconds to approve on phone)
    print("Waiting for Duo 2FA... Please approve the notification on your phone.")
    time.sleep(15)  # Wait for 15 seconds to give time for the push notification to be approved

    # Handle "Stay signed in?" Page (If It Appears)
    try:
        stay_signed_in = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "idSIButton9")))
        stay_signed_in.click()
    except:
        print("Stay signed in prompt did not appear.")

    # Wait for Blackboard dashboard to load
    time.sleep(5)

    # Step 5: Extract Course Titles
    course_cards = driver.find_elements(By.CSS_SELECTOR, "bb-base-course-card")

    if course_cards:
        print("Courses Found:")
        for card in course_cards:
            # Extract the course title from the nested structure
            course_title_element = card.find_element(By.CSS_SELECTOR, "h4.js-course-title-element")
            print(course_title_element.text)
    else:
        print("No courses found. Check the class name for course titles.")


except Exception as e:
    print(f"Error: {e}")

finally:
    driver.quit()
