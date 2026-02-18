# 🍽️ Recipe Generator

A smart recipe discovery app built with **Streamlit**, powered by the **Spoonacular API**. Search any dish and instantly get full recipes with ingredients, step-by-step instructions, nutrition facts, and a serving scaler.

---

## What It Does

- Search any dish by name and get a matching recipe instantly
- Scale ingredients and nutrition automatically based on desired servings
- View full step-by-step cooking instructions
- See detailed nutrition breakdown: calories, protein, carbs, fat, sugar, fiber
- Dietary badges: Vegetarian, Vegan, Gluten-Free, Dairy-Free, Very Healthy
- Price per serving shown in both USD and Nepali Rupees (NPR)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Recipe Data | Spoonacular API |
| Language | Python |

---

## Project Structure

```
RecipeGenerator/
│
├── app.py               ← Main Streamlit app
├── requirements.txt     ← Python dependencies
├── .env                 ← Your API key (never share or commit this)
├── .env.example         ← Safe template to share
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Step 1 — Get a Spoonacular API Key

1. Go to [spoonacular.com/food-api](https://spoonacular.com/food-api)
2. Sign up for a free account
3. Copy your API key from the dashboard

### Step 2 — Store Your API Key Safely

Create a `.env` file in your project folder:

```
SPOONACULAR_API_KEY=your_api_key_here
```

Then load it in `app.py` like this:

```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SPOONACULAR_API_KEY")
```

> ⚠️ Never hardcode your API key in the source code. Never commit `.env` to GitHub.

### Step 3 — Install Dependencies

```powershell
pip install streamlit requests python-dotenv
```

### Step 4 — Run the App

```powershell
streamlit run app.py
```

Opens automatically at `http://localhost:8501`

---

## How to Use

1. Enter a dish name in the sidebar (e.g. `lentil soup`, `chocolate cake`, `momo`)
2. Set your desired number of servings using the number input
3. Click **Generate Recipe**
4. Browse ingredients, instructions, and nutrition — all scaled to your servings

---

## Spoonacular API Endpoints Used

### 1. Complex Search
```
GET https://api.spoonacular.com/recipes/complexSearch?query={dish}&apiKey={key}
```
Finds a recipe ID matching the searched dish name.

### 2. Recipe Information
```
GET https://api.spoonacular.com/recipes/{id}/information?includeNutrition=true&apiKey={key}
```
Returns full recipe details: ingredients, instructions, nutrition, dietary flags, price.

---

## Free Tier Limits (Spoonacular)

| Limit | Amount |
|---|---|
| Requests per day | 150 |
| Nutrition data | ✅ Included |
| Images | ✅ Included |

The free tier is sufficient for personal use and development.

---

## Features in Detail

### Serving Scaler
Set any number of servings and all ingredient quantities and nutritional values adjust automatically. If a recipe serves 4 and you need 1, every measurement is divided by 4.

### Nutrition Panel
Displays scaled values per serving for:
- 🔥 Calories
- 🥩 Protein (g)
- 🍞 Carbohydrates (g)
- 🧈 Fat (g)
- 🍬 Sugar (g)
- 🌾 Fiber (g)

### Price Per Serving
Shown in USD and converted to Nepali Rupees (NPR) at Rs. 140 = $1.

### Dietary Badges
Automatically displayed if the recipe is Vegetarian, Vegan, Gluten-Free, Dairy-Free, or Very Healthy.

---

## Security Notes

- Store your API key in `.env` only — never in `app.py`
- Add `.env` to `.gitignore` before pushing to GitHub
- If your key is ever exposed, regenerate it immediately at [spoonacular.com/food-api/console](https://spoonacular.com/food-api/console)

---

## Planned Upgrades

- [ ] Search by ingredient ("what's in my fridge?")
- [ ] Filter by dietary preference (vegan, gluten-free, etc.)
- [ ] Save favourite recipes locally
- [ ] Compare two recipes side by side
- [ ] Export recipe as PDF
- [ ] Connect to Restaurant Finder — "Can't cook? Find this dish near you"

---

## Related Project

**[Restaurant Finder](../RestaurantFinder/)** — a companion app to discover nearby restaurants by location, powered by OpenStreetMap. No API key or billing required.

---

*Built with Streamlit · Powered by Spoonacular API*
