# # main.py

# from fastapi import FastAPI, Query, HTTPException
# from test import perform_search
# from enum import Enum

# app = FastAPI()

# class SellerType(str, Enum):
#     all = "all"
#     owner = "owner"
#     dealer = "dealer"

# @app.get("/search")
# async def search(
#     query: str = Query(..., description="Search query"),
#     seller_type: SellerType = Query(SellerType.all, description="Type of seller (all, owner, or dealer)")
# ):
#     result = perform_search(query)
#     if "error" in result:
#         raise HTTPException(status_code=500, detail=result["error"])
#     return result



# main.py
# from fastapi import FastAPI, HTTPException, Query
# from typing import List, Optional
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
# import time

from fastapi import FastAPI, Query, HTTPException
from typing import List, Optional
from a import perform_search
from enum import Enum

app = FastAPI()

class SellerType(str, Enum):
    all = 'all'
    owner = 'owner'
    dealer = 'dealer'

@app.get("/search", response_model=List[dict])
async def search(query: str, seller_type: SellerType = SellerType.all):
    try:
        search_results = perform_search(query=query, seller_type=seller_type.value)
        return search_results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))