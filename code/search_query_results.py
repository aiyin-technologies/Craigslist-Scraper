# modules.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_link(result):
    try:
        return WebDriverWait(result, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.cl-app-anchor"))
        ).get_attribute('href')
        # return EC.presence_of_element_located((By.CSS_SELECTOR, "a.cl-app-anchor")).get_attribute('href')
    except (NoSuchElementException, StaleElementReferenceException, TimeoutException):
        return None

def perform_search(query: str, seller_type: str = 'all'):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
    })

    try:
        driver_path = r"D:\Haroon\Career\Internships\Gear Trybe Inc\code\chromedriver-win64\chromedriver.exe"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        return {"error": f"Error setting up ChromeDriver: {str(e)}"}
    
    try:
        base_url = "https://sfbay.craigslist.org/search/sss?excats=5-2-13-22-26-1-26-1-1-1-3-6-11-1-5-8-1-1-1-1-1-4-1-7-1-10-2-2-2-1-1-1-1-1-1-2-3-1-1-2-2-1-1-2-1-2-1-1-1-1-1-1-3-1-1-1-1-1-4-1"
        
        url = f"{base_url}&{'purveyor=' + seller_type + '&' if seller_type in ['owner', 'dealer'] else ''}query={query}"
        
        driver.get(url)
        
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "li.cl-search-result"))
            )
            
            results = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result"))
            )
            
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_link = {executor.submit(extract_link, result): result for result in results}
                result_links = [future.result() for future in as_completed(future_to_link) if future.result()]
            
            if not result_links:
                return {"query": query, "seller_type": seller_type, "results": "No results found"}
            
            return {"query": query, "seller_type": seller_type, "results": result_links}
        
        except TimeoutException:
            return {"query": query, "seller_type": seller_type, "error": "Page took too long to load"}
        except Exception as e:
            return {"query": query, "seller_type": seller_type, "error": f"Error extracting results: {str(e)}"}
    
    finally:
        driver.quit()