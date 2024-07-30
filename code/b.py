from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Union
from enum import Enum
import asyncio
import uvicorn
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import json
import pickle
import os
import uuid

app = FastAPI()

class SellerType(str, Enum):
    all = 'all'
    owner = 'owner'
    dealer = 'dealer'

class SearchResult(BaseModel):
    title: str
    email: str
    phone_number: str
    result_url: str

class CaptchaRequired(BaseModel):
    status: str
    session_id: str

class CaptchaSolution(BaseModel):
    session_id: str
    solution: str

# Global dictionary to store session information
sessions = {}

def get_driver(load_cookies=False):
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    chrome_options.add_argument('--proxy-server=5.58.33.187:5678')


    chrome_options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2,
    })
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('log-level=3')

    driver = webdriver.Chrome(service=Service(), options=chrome_options)

    if load_cookies and os.path.exists("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        driver.get("https://sfbay.craigslist.org")
        for cookie in cookies:
            driver.add_cookie(cookie)

    return driver

def captcha_detected(driver):
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "cf-hcaptcha-container"))
        )
        return True
    except:
        return False

async def perform_search(query: str, session_id: Optional[str] = None, seller_type: str = 'all', max_retries: int = 3):
    driver = get_driver(load_cookies=True)
    results = []

    try:
        base_url = "https://sfbay.craigslist.org/search/sss?excats=5-2-13-22-26-1-26-1-1-1-3-6-11-1-5-8-1-1-1-1-1-4-1-7-1-10-2-2-2-1-1-1-1-1-1-2-3-1-1-2-2-1-1-2-1-2-1-1-1-1-1-1-3-1-1-1-1-1-4-1"
        url = f"{base_url}&{'purveyor=' + seller_type + '&' if seller_type in ['owner', 'dealer'] else ''}query={query}"
        
        current_url = f"{url}#search=1~gallery~0~0"
        print("Processing page 1")
        driver.get(current_url)

        if captcha_detected(driver):
            if session_id:
                sessions[session_id]["driver"] = driver
            else:
                session_id = str(uuid.uuid4())
                sessions[session_id] = {"driver": driver, "query": query, "seller_type": seller_type}
            return {"status": "captcha_required", "session_id": session_id}

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
                        
                        if captcha_detected(driver):
                            driver.close()
                            driver.switch_to.window(driver.window_handles[0])
                            if session_id:
                                sessions[session_id]["driver"] = driver
                            else:
                                session_id = str(uuid.uuid4())
                                sessions[session_id] = {"driver": driver, "query": query, "seller_type": seller_type}
                            return {"status": "captcha_required", "session_id": session_id}
                        
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

                            await asyncio.sleep(15)

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

                        await asyncio.sleep(5)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        
                        break
                    except (StaleElementReferenceException, TimeoutException) as e:
                        print(f"Attempt {attempt + 1} failed: {str(e)}")
                        if attempt == max_retries - 1:
                            print(f"Max retries reached for result {index}. Moving to next.")
                        driver.get(current_url)
                        await asyncio.sleep(2)

        except TimeoutException:
            print("No results found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
    
    finally:
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        driver.quit()

    return results

@app.get("/search", response_model=Union[List[SearchResult], CaptchaRequired])
async def search(query: str,background_tasks: BackgroundTasks, seller_type: SellerType = SellerType.all):
    try:
        search_results = await perform_search(query=query, seller_type=seller_type.value)
        if isinstance(search_results, dict) and search_results.get("status") == "captcha_required":
            return CaptchaRequired(**search_results)
        return [SearchResult(**result) for result in search_results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/solve_captcha", response_model=Union[List[SearchResult], CaptchaRequired])
async def solve_captcha(captcha_solution: CaptchaSolution):
    if captcha_solution.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session = sessions[captcha_solution.session_id]
    driver = session["driver"]
    
    try:
        # Here you would typically interact with the captcha element to input the solution
        # Since we can't actually solve the captcha programmatically, we'll just simulate it
        print(f"Applying captcha solution: {captcha_solution.solution}")
        await asyncio.sleep(2)  # Simulating captcha solving time
        
        # After "solving" the captcha, continue with the search
        search_results = await perform_search(
            query=session["query"],
            seller_type=session["seller_type"],
            session_id=captcha_solution.session_id
        )
        
        if isinstance(search_results, dict) and search_results.get("status") == "captcha_required":
            return CaptchaRequired(**search_results)
        return [SearchResult(**result) for result in search_results]
    finally:
        # Clean up the session
        del sessions[captcha_solution.session_id]