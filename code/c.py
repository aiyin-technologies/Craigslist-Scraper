import random
import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

# Proxy list
proxy_list = [
    "50.218.57.65:80",
    "51.254.78.223:80",
    "198.44.255.3:80",
    "47.74.40.128:7788",
    "116.203.28.43:80",
    "195.39.194.8:80",
    "12.186.205.122:80",
    "8.223.31.16:80",
    "200.25.254.193:54240",
    "72.10.160.90:1365",
    "93.177.67.178:80",
    "67.43.227.228:23737",
    "103.105.196.30:80",
    "50.218.57.74:80",
    "103.137.62.253:80",
    "91.92.155.207:3128",
    "139.99.237.62:80",
    "20.24.43.214:80",
    "194.182.187.78:3128",
    "175.139.233.76:80",
    "50.220.168.134:80",
    "23.247.136.252:80",
    "50.218.57.70:80",
    "66.191.31.158:80",
    "212.107.28.120:80",
    "198.176.58.44:80",
    "18.130.192.203:1080",
    "155.94.241.131:3128",
    "47.74.152.29:8888",
    "154.203.132.55:8090",
    "189.232.204.95:3128",
    "20.210.113.32:8123",
    "167.102.133.97:80",
    "122.200.19.103:80",
    "160.86.242.23:8080",
    "210.247.252.133:3127",
    "67.43.228.253:12915",
    "51.15.242.202:8888",
    "216.137.184.253:80",
    "50.222.245.43:80",
    "50.175.212.72:80",
    "50.223.38.6:80",
    "50.231.110.26:80",
    "50.223.239.167:80",
    "50.168.72.115:80",
    "50.174.7.152:80",
    "50.239.72.17:80",
    "50.218.204.96:80",
    "50.221.74.130:80",
    "50.174.7.162:80",
    "50.168.72.118:80",
    "50.171.122.30:80",
    "50.172.75.126:80"
    "50.168.72.112:80",
    "50.174.7.159:80",
    "50.222.245.46:80",
    "50.218.57.68:80",
    "144.126.216.57:80,"
    "32.223.6.94:80",
    "50.218.57.64:80",
    "50.174.145.9:80",
    "50.174.7.153:80",
    "139.60.209.2:80",
    "50.217.226.47:80",
    "50.169.37.50:80",
    "50.217.226.45:80",
    "50.168.72.114:80",
    "50.207.199.81:80",
    "198.16.63.10:80",
    "50.239.72.18:80",
    "50.175.212.77:80",
    "50.174.7.157:80",
    "50.169.135.10:80",
    "50.222.245.50:80",
    "50.144.166.226:80",
    "50.144.168.74:80",
    "50.174.7.158:80",
    "50.207.199.83:80",
    "50.171.187.51:80",
    "50.222.245.47:80",
    "50.175.212.76:80",
    "47.252.29.28:11222",
    "50.230.222.202:80",
    "50.222.245.40:80",
    "50.172.75.127:80",
    "50.174.145.15:80",
    "50.172.75.123:80"
    "50.174.7.156:80",
    "50.218.57.66:80",
    "50.174.145.12:80",
    "50.168.72.116:80",
    "50.223.239.166:80",
    "50.207.199.82:80",
    "50.174.145.8:80",
    "50.217.226.44:80",
    "50.207.199.80:80",
    "50.171.187.50:80",
    "50.174.7.154:80",
    "50.144.189.54:80",
    "50.168.72.117:80",
    "125.25.32.66:8080",
    "174.138.19.138:9090,"
    "174.138.20.66:9090",
    "103.154.91.250:8081",
    "45.136.198.90:3128",
    "123.202.159.223:80",
    "38.54.71.67:80",
    "123.30.154.171:7777",
    "210.247.252.6:3127",
    "223.135.156.183:8080",
    "189.240.60.169:9090",
    "135.148.233.152:3129",
    "84.39.112.144:3128",
    "189.240.60.163:9090"
    "20.206.106.192:8123",
    "217.182.55.226:80",
    "210.247.252.23:3127",
    "139.162.78.109:8080",
    "162.245.85.220:80",
    # 119.59.124.119:8888
    # 116.125.141.115:80
    # 189.240.60.164:9090
    # 24.199.84.240:3128
    # 154.208.10.126:80
    # 125.212.231.103:808
    # 12.186.205.121:80
    # 194.182.163.117:3128
    # 200.174.198.86:8888
    # 200.119.44.50:9090
    # 13.83.94.137:3128
    # 167.99.124.118:80
    # 189.240.60.168:9090
    # 176.9.238.155:16379
    # 72.10.160.170:2657
    # 210.247.253.172:3127
    # 67.43.228.254:2679
    # 176.65.240.15:80
    # 8.219.97.248:80
    # 159.203.61.169:3128
    # 47.90.205.231:33333
    # 162.240.76.92:80
    # 185.160.26.114:80
    # 47.88.31.196:8080
    # 134.209.29.120:8080
    # 210.247.252.16:3127
    # 207.148.71.74:80
    # 64.227.6.0:4003
    # 35.185.196.38:3128
    # 89.145.162.81:3128
    # 23.247.136.245:80
    # 5.196.65.71:3128
    # 149.56.148.20:80
    # 203.77.215.45:10000
    # 162.240.75.37:80
    # 189.240.60.166:9090
    # 179.191.39.221:3128
    # 72.10.164.178:1417
    # 197.255.126.69:80
    # 103.174.102.127:80
    # 50.239.72.16:80
    # 50.218.204.99:80
    # 47.251.43.115:33333
    # 50.223.246.237:80
    # 50.218.204.103:80
    # 50.223.242.97:80
    # 119.252.167.130:41890
    # 200.24.138.204:999
    # 47.252.18.37:8443
    # 86.101.159.147:18080
    # 139.59.1.14:8080
    # 161.35.70.249:3128
    # 163.172.33.137:4000
    # 135.148.171.194:18080
    # 47.251.70.179:80
    # 45.77.147.46:3128
    # 94.101.185.188:13699
    # 65.108.9.181:80
    # 12.186.205.120:80
    # 138.68.235.51:80
    # 116.202.14.132:80
    # 41.86.229.25:8888
    # 51.89.255.67:80
    # 178.128.113.118:23128
    # 50.223.239.168:80
    # 50.175.212.74:80
    # 50.223.242.100:80
    # 50.168.72.113:80
    # 50.218.204.106:80
    # 50.222.245.41:80
    # 50.222.245.44:80
    # 50.223.242.103:80
    # 50.223.239.173:80
    # 50.223.239.183:80
    # 188.163.170.130:41209
    # 202.52.12.86:8080
    # 217.197.237.74:8080
    # 103.168.129.124:8080
    # 46.161.194.88:8085
    # 45.184.152.145:999
    # 85.117.56.151:8080
    # 67.43.228.251:3343
    # 1.32.59.217:47045
    # 210.247.252.113:3127
    # 130.61.120.213:8888
    # 103.174.238.233:8181
    # 130.0.234.31:8080
    # 50.172.75.121:80
    # 50.168.72.122:80
    # 50.175.212.66:80
    # 50.239.72.19:80
    # 50.222.245.42:80
    # 50.172.75.125:80
    # 50.172.75.120:80
    # 50.175.212.79:80
    # 96.113.158.126:80
    # 127.0.0.7:80
    # 50.174.145.11:80
    # 50.218.57.67:80
    # 50.217.226.43:80
    # 50.217.226.42:80
    # 50.202.75.26:80
    # 50.223.239.165:80
    # 50.223.239.185:80
    # 103.168.44.191:8083
    # 191.102.248.8:8085
    # 38.63.212.221:3128
    # 91.231.61.225:443
    # 80.87.178.175:8080
    # 186.192.78.5:8080
    # 185.153.44.81:8080
    # 50.174.145.10:80
    # 185.174.136.29:80
    # 49.245.96.145:80
    # 211.128.96.206:80
    # 198.49.68.80:80
    # 15.204.168.178:8888
    # 50.222.245.45:80
    # 83.1.176.118:80
    # 195.23.57.78:80
    # 50.223.239.191:80
    # 191.96.243.81:80
    # 185.217.143.96:80
    # 178.236.247.235:80
    # 50.223.239.161:80
    # 68.185.57.66:80
    # 51.89.14.70:80
    # 50.223.239.160:80
    # 64.206.77.122:3128
    # 50.174.145.13:80
    # 50.231.104.58:80
    # 50.122.86.118:80
    # 181.78.64.172:999
    # 102.213.84.250:8080
    # 181.10.160.155:8080
    # 152.32.67.107:65535
    # 103.36.8.55:8181
    # 50.172.39.98:80
    # 50.217.226.41:80
    # 67.43.236.20:10145
    # 50.172.75.122:80
    # 72.10.160.171:10095
    # 50.223.239.175:80
    # 50.223.246.226:80
    # 50.217.226.40:80
    # 50.221.230.186:80
    # 104.165.127.65:3128
    # 104.252.131.94:3128
    # 154.201.63.119:3128
    # 181.209.96.157:999
    # 154.202.96.57:3128
    # 154.29.232.142:6802
    # 198.37.98.216:5746
    # 154.202.120.63:3128
    # 154.202.108.239:3128
    # 154.202.97.90:3128
    # 156.239.53.130:3128
    # 154.202.120.133:3128
    # 154.202.122.87:3128
    # 69.58.9.169:7239
    # 45.61.124.56:6385
    # 154.201.62.249:3128
    # 104.164.183.101:3128
    # 198.144.190.126:5973
    # 156.239.49.109:3128
    # 154.202.107.54:3128
    # 166.159.90.56:53281
    # 154.202.98.121:3128
    # 198.46.137.164:6368
    # 134.73.104.231:6865
    # 50.117.66.111:3128
    # 104.252.131.13:3128
    # 154.202.120.87:3128
    # 154.202.121.130:3128
    # 156.239.52.246:3128
    # 142.147.242.212:6191
    # 142.147.245.69:5760
    # 206.206.69.246:6510
    # 198.46.202.207:5487
    # 154.201.61.131:3128
    # 154.202.96.65:3128"
]

def get_random_proxy(proxy_list):
    return random.choice(proxy_list)

def test_proxy(proxy):
    try:
        response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=10)
        return response.status_code == 200
    except:
        return False

def perform_search(query: str, seller_type: str = 'all', max_retries: int = 3):
    results = []
    
    for attempt in range(max_retries):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-javascript")

            # Use a random proxy
            proxy = get_random_proxy(working_proxies)
            chrome_options.add_argument(f'--proxy-server={proxy}')

            chrome_options.add_experimental_option("prefs", {
                "profile.managed_default_content_settings.images": 2,
            })
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_argument('log-level=3')  # Only show fatal errors

            service = Service()
            driver = webdriver.Chrome(service=service, options=chrome_options)

            base_url = "https://sfbay.craigslist.org/search/sss?excats=5-2-13-22-26-1-26-1-1-1-3-6-11-1-5-8-1-1-1-1-1-4-1-7-1-10-2-2-2-1-1-1-1-1-1-2-3-1-1-2-2-1-1-2-1-2-1-1-1-1-1-1-3-1-1-1-1-1-4-1"
            url = f"{base_url}&{'purveyor=' + seller_type + '&' if seller_type in ['owner', 'dealer'] else ''}query={query}"
            
            current_url = f"{url}#search=1~gallery~0~0"
            print(f"Processing page 1 with proxy {proxy}")
            driver.get(current_url)
            
            try:
                result_links = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.cl-search-result a.cl-app-anchor"))
                )
                
                for index, link in enumerate(result_links, 1):
                    for link_attempt in range(max_retries):
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
                            print(f"Attempt {link_attempt + 1} failed for result {index}: {str(e)}")
                            if link_attempt == max_retries - 1:
                                print(f"Max retries reached for result {index}. Moving to next.")
                            driver.get(current_url)
                            time.sleep(2)

            except TimeoutException:
                print("No results found.")
            except Exception as e:
                print(f"An error occurred: {str(e)}")
        
            driver.quit()
            return results  # If successful, return the results

        except Exception as e:
            print(f"Attempt {attempt + 1} failed with proxy {proxy}: {str(e)}")
            if attempt == max_retries - 1:
                print("Max retries reached. Returning current results.")
            else:
                print("Retrying with a different proxy...")
    
    return results  # Return current results if all attempts fail

# Test and filter working proxies
print("Testing proxies...")
working_proxies = [proxy for proxy in proxy_list if test_proxy(proxy)]
print(f"Working proxies: {len(working_proxies)}/{len(proxy_list)}")

# Example usage
search_results = perform_search("needs transmission")

# Write results to JSON file
with open('leads1.json', 'w') as json_file:
    json.dump(search_results, json_file, indent=4)

print(f"Results written to leads1.json")