from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import random

app = FastAPI(
    title="Recipe API",
    description="Recipe API powered by API-Ninjas",
    version="2.0"
)

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API-Ninjas Configuration
# -----------------------------
API_NINJAS_URL = "https://api.api-ninjas.com/v3/recipe"
API_KEY = "vL4tGjllsILlRBX40tbSe0zubaJcLyNfy5a5naFj"  # Keep secure in production

HEADERS = {
    "X-Api-Key": API_KEY
}

def fetch_recipes(params: dict) -> list:
    """Helper to call API-Ninjas and return results."""
    try:
        response = requests.get(API_NINJAS_URL, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Upstream API error: {e}")

# -----------------------------
# API Endpoints
# -----------------------------

@app.get("/search")
def search(query: str):
    """Search recipes by dish title."""
    results = fetch_recipes({"title": query})
    return {"results": results}


@app.get("/ingredient/{ingredient_name}")
def search_by_ingredient(ingredient_name: str):
    """Search recipes by ingredient name (uses title search as fallback for free tier)."""
    results = fetch_recipes({"title": ingredient_name})
    return {"results": results}


@app.get("/random")
def random_recipe():
    """Return a random recipe by picking from a list of common dishes."""
    common_dishes = [
        "pasta", "chicken", "salad", "soup", "cake",
        "pizza", "burger", "steak", "curry", "tacos",
        "sushi", "sandwich", "omelette", "pancakes", "risotto"
    ]
    dish = random.choice(common_dishes)
    results = fetch_recipes({"title": dish})
    if results:
        return {"results": [random.choice(results)]}
    return {"results": []}
