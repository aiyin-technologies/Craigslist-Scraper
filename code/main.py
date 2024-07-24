# main.py

from fastapi import FastAPI, Query, HTTPException
from search_query_results import perform_search
from enum import Enum

app = FastAPI()

class SellerType(str, Enum):
    all = "all"
    owner = "owner"
    dealer = "dealer"

@app.get("/search")
async def search(
    query: str = Query(..., description="Search query"),
    seller_type: SellerType = Query(SellerType.all, description="Type of seller (all, owner, or dealer)")
):
    result = perform_search(query, seller_type.value)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result