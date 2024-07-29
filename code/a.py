# a.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import json

def perform_search(query: str, seller_type: str = 'all', max_retries: int = 3):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
    })
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('log-level=3')  # Only show fatal errors

    results = []

    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error setting up ChromeDriver: {str(e)}")
        return results
    
    try:
        base_url = "https://sfbay.craigslist.org/search/sss?excats=5-2-13-22-26-1-26-1-1-1-3-6-11-1-5-8-1-1-1-1-1-4-1-7-1-10-2-2-2-1-1-1-1-1-1-2-3-1-1-2-2-1-1-2-1-2-1-1-1-1-1-1-3-1-1-1-1-1-4-1"
        url = f"{base_url}&{'purveyor=' + seller_type + '&' if seller_type in ['owner', 'dealer'] else ''}query={query}"
        
        current_url = f"{url}#search=1~gallery~0~0"
        print("Processing page 1")
        driver.get(current_url)
        
        try:
            result_links = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result a.cl-app-anchor"))
            )
            
            for index, link in enumerate(result_links, 1):
                for attempt in range(max_retries):
                    try:
                        href = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, f"li.cl-search-result:nth-child({index}) a.cl-app-anchor"))
                        ).get_attribute('href')
                        
                        print(f"Processing result {index} on page 1")
                        
                        driver.execute_script("window.open('');")
                        driver.switch_to.window(driver.window_handles[-1])
                        driver.get(href)
                        
                        WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
                        )
                        
                        result = {
                            "title": "none",
                            "email": "none",
                            "phone_number": "none",
                            "result_url": href
                        }

                        try:
                            title_element = WebDriverWait(driver, 5).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.postingtitle"))
                            )
                            result["title"] = title_element.text
                        except Exception:
                            print(f"Failed to extract title for result {index}")

                        try:
                            reply_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.reply-button-row button"))
                            )
                            driver.execute_script("arguments[0].click();", reply_button)
                            print(f"Successfully clicked reply button for result {index}")

                            email_button = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "div.reply-option-section.collapsed button"))
                            )
                            driver.execute_script("arguments[0].click();", email_button)
                            print(f"Successfully clicked email button for result {index}")

                            try:
                                email_element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.reply-content.reply-content-email a"))
                                )
                                result["email"] = email_element.text
                                print(f"Email found: {result['email']}")
                            except Exception as email_error:
                                print(f"Failed to find email for result {index}: {str(email_error)}")

                            try:
                                phone_element = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.reply-content.reply-content-phone a"))
                                )
                                result["phone_number"] = phone_element.text
                                print(f"Phone number found: {result['phone_number']}")
                            except Exception as phone_error:
                                print(f"Failed to find phone number for result {index}: {str(phone_error)}")

                        except Exception as click_error:
                            print(f"Failed to click reply or email button for result {index}: {str(click_error)}")

                        results.append(result)

                        time.sleep(5)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                        break
                    except (StaleElementReferenceException, TimeoutException) as e:
                        print(f"Attempt {attempt + 1} failed: {str(e)}")
                        if attempt == max_retries - 1:
                            print(f"Max retries reached for result {index}. Moving to next.")
                        driver.get(current_url)
                        time.sleep(2)

        except TimeoutException:
            print("No results found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    finally:
        driver.quit()

    return results

# # Example usage
# search_results = perform_search("needs transmission")

# # Write results to JSON file
# with open('leads1.json', 'w') as json_file:
#     json.dump(search_results, json_file, indent=4)

# print(f"Results written")