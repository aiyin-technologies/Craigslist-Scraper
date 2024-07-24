# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
# import time

# def perform_search(query: str, seller_type: str = 'all', max_retries: int = 3):
#     chrome_options = Options()
#     # chrome_options.add_argument("--headless")  # Run in headless mode
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_experimental_option("prefs", {
#         "profile.managed_default_content_settings.images": 2,
#     })

#     try:
#         service = Service()  # Let Selenium find the appropriate driver
#         driver = webdriver.Chrome(service=service, options=chrome_options)
#     except Exception as e:
#         print(f"Error setting up ChromeDriver: {str(e)}")
#         return
    
#     try:
#         base_url = "https://sfbay.craigslist.org/search/sss?excats=5-2-13-22-26-1-26-1-1-1-3-6-11-1-5-8-1-1-1-1-1-4-1-7-1-10-2-2-2-1-1-1-1-1-1-2-3-1-1-2-2-1-1-2-1-2-1-1-1-1-1-1-3-1-1-1-1-1-4-1"
#         url = f"{base_url}&{'purveyor=' + seller_type + '&' if seller_type in ['owner', 'dealer'] else ''}query={query}"
        
#         driver.get(url)
        
#         page_number = 1
#         while True:
#             print(f"Processing page {page_number}")
#             try:
#                 # Wait for the results to load
#                 result_links = WebDriverWait(driver, 10).until(
#                     EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result a.cl-app-anchor"))
#                 )
                
#                 for index, link in enumerate(result_links, 1):
#                     for attempt in range(max_retries):
#                         try:
#                             # Get the href attribute
#                             href = link.get_attribute('href')
#                             print(f"Processing result {index} on page {page_number}")
                            
#                             # Navigate to the link in a new tab
#                             driver.execute_script("window.open('');")
#                             driver.switch_to.window(driver.window_handles[-1])
#                             driver.get(href)
                            
#                             # Wait for 5 seconds (reduced from 10)
#                             time.sleep(5)
                            
#                             # Close the tab and switch back to the main window
#                             driver.close()
#                             driver.switch_to.window(driver.window_handles[0])
                            
#                             # Re-find the elements to avoid stale element references
#                             result_links = WebDriverWait(driver, 10).until(
#                                 EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result a.cl-app-anchor"))
#                             )
#                             break  # If successful, break the retry loop
#                         except (StaleElementReferenceException, TimeoutException) as e:
#                             print(f"Attempt {attempt + 1} failed: {str(e)}")
#                             if attempt == max_retries - 1:  # If this was the last retry
#                                 print(f"Max retries reached for result {index}. Moving to next.")
#                             driver.get(url)  # Go back to the main results page
#                             time.sleep(2)  # Wait for the page to reload
                
#                 # Try to find the "next" button and get its href
#                 try:
#                     next_button = WebDriverWait(driver, 10).until(
#                         EC.presence_of_element_located((By.CSS_SELECTOR, "a.next[href^='https://sfbay.craigslist.org/']"))
#                     )
#                     next_page_url = next_button.get_attribute('href')
#                     driver.get(next_page_url)
#                     page_number += 1
#                 except (TimeoutException, NoSuchElementException):
#                     # If there's no next button, we've reached the end
#                     print("Finished navigating through all results.")
#                     break
                
#             except Exception as e:
#                 print(f"An error occurred: {str(e)}")
#                 break
    
#     finally:
#         driver.quit()

# # Example usage
# perform_search("needs engine")



from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time

def perform_search(query: str, seller_type: str = 'all', max_retries: int = 3):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
    })

    try:
        service = Service()  # Let Selenium find the appropriate driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        print(f"Error setting up ChromeDriver: {str(e)}")
        return
    
    try:
        base_url = "https://sfbay.craigslist.org/search/sss?excats=5-2-13-22-26-1-26-1-1-1-3-6-11-1-5-8-1-1-1-1-1-4-1-7-1-10-2-2-2-1-1-1-1-1-1-2-3-1-1-2-2-1-1-2-1-2-1-1-1-1-1-1-3-1-1-1-1-1-4-1"
        url = f"{base_url}&{'purveyor=' + seller_type + '&' if seller_type in ['owner', 'dealer'] else ''}query={query}"
        
        driver.get(url)
        
        while True:
            print(f"Processing page")
            try:
                # Wait for the results to load
                result_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result a.cl-app-anchor"))
                )
                
                for index, link in enumerate(result_links, 1):
                    for attempt in range(max_retries):
                        try:
                            # Get the href attribute
                            href = link.get_attribute('href')
                            print(f"Processing result {index} on page")
                            
                            # Navigate to the link in a new tab
                            driver.execute_script("window.open('');")
                            driver.switch_to.window(driver.window_handles[-1])
                            driver.get(href)
                            
                            # Wait for 5 seconds (reduced from 10)
                            time.sleep(5)
                            
                            # Close the tab and switch back to the main window
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            
                            # Re-find the elements to avoid stale element references
                            result_links = WebDriverWait(driver, 15).until(
                                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result a.cl-app-anchor"))
                            )
                            break  # If successful, break the retry loop
                        except (StaleElementReferenceException, TimeoutException) as e:
                            print(f"Attempt {attempt + 1} failed: {str(e)}")
                            if attempt == max_retries - 1:  # If this was the last retry
                                print(f"Max retries reached for result {index}. Moving to next.")
                            driver.get(url)  # Go back to the main results page
                            time.sleep(2)  # Wait for the page to reload
                
                # Try to find the "next" button and get its href
                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "a.next[href^='https://sfbay.craigslist.org/']"))
                    )
                    next_page_url = next_button.get_attribute('href')
                    driver.get(next_page_url)
                except (TimeoutException, NoSuchElementException):
                    # If there's no next button, we've reached the end
                    print("Finished navigating through all results.")
                    break
                
            except Exception as e:
                print(f"An error occurred: {str(e)}")
                break
    
    finally:
        driver.quit()

# Example usage
perform_search("needs transmission")
