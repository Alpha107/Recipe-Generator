# 🍜 Restaurant Finder

A location-based restaurant discovery app built with **FastAPI + Streamlit**, powered entirely by free and open data sources. No API key. No billing. No credit card.

---

## What It Does

- Search restaurants near any location in the world
- Filter by search radius and cuisine keyword
- View distance and travel time to each restaurant
- Click any restaurant for full details: opening hours, phone, website, cuisine type
- Sorted by distance from your searched location
- Works with Nepali place names and scripts

---

## Tech Stack

| Layer | Technology | Cost |
|---|---|---|
| Backend | FastAPI + Uvicorn | Free |
| Frontend | Streamlit | Free |
| Geocoding | Nominatim (OpenStreetMap) | Free |
| Restaurant Data | Overpass API (OpenStreetMap) | Free |
| Distance & Routing | OSRM | Free |

**No Google Maps. No API key. No payment method required.**

---

## Project Structure

```
RestaurantFinder/
│
├── backend/
│   ├── main.py          ← FastAPI app (all API endpoints)
│   ├── services.py      ← Nominatim, Overpass, OSRM calls
│   └── requirements.txt
│
├── frontend/
│   ├── app.py           ← Streamlit UI
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.8 or higher
- pip

Check your Python version:
```powershell
python --version
```

---

### Step 1 — Set Up the Backend

Open a terminal and run:

```powershell
cd E:\RestaurantFinder\backend
pip install fastapi uvicorn requests
uvicorn main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Leave this terminal open.

---

### Step 2 — Set Up the Frontend

Open a **second terminal** and run:

```powershell
cd E:\RestaurantFinder\frontend
pip install streamlit requests
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`

---

### Step 3 — Test the Backend Directly (Optional)

Open this URL in your browser to confirm the backend is working:

```
http://127.0.0.1:8000/restaurants?location=Thamel,Kathmandu
```

You should see a JSON response with restaurant names, distances, and details.

---

## API Endpoints

### Search restaurants near a location

```
GET /restaurants?location=Thamel,Kathmandu&radius=2000&keyword=momo
```

| Parameter | Type | Required | Description |
|---|---|---|---|
| location | string | ✅ Yes | Any place name or address |
| radius | integer | No | Search radius in meters (default: 2000) |
| keyword | string | No | Filter by name or cuisine (e.g. pizza, momo) |

**Example response:**
```json
{
  "query_location": "Thamel, Kathmandu, Nepal",
  "count": 15,
  "results": [
    {
      "name": "Everest Steak House",
      "cuisine": "steak",
      "distance": "958 m",
      "duration": "2 mins",
      "opening_hours": ["Mo-Su 10:00-22:00"]
    }
  ]
}
```

---

### Get full details for a restaurant

```
GET /restaurant/{place_id}
```

Returns: name, cuisine, address, phone, website, email, opening hours, takeaway, delivery, wheelchair access, OpenStreetMap link.

---

## How the Data Flow Works

```
User enters location
        ↓
Nominatim converts it to lat/lng coordinates
        ↓
Overpass API finds all restaurants within the radius
        ↓
OSRM calculates driving distance and time to each one
        ↓
Results sorted by distance and displayed in the UI
        ↓
User clicks a restaurant → Overpass fetches full details
```

---

## Known Limitations

| Limitation | Reason |
|---|---|
| No restaurant photos | OpenStreetMap does not store images |
| Slow first load (15–30 sec) | Overpass API is a free community server |
| Some restaurants missing info | OSM data depends on community contributions |
| Occasional timeouts | Free Overpass servers get congested |

The app automatically tries 3 different Overpass servers if one fails.

---

## Planned Upgrades

- [ ] Show restaurants on an interactive map (Folium)
- [ ] "Open Now" filter based on current time
- [ ] User authentication and saved favourites
- [ ] AI-powered "What should I eat tonight?" recommender
- [ ] Export results to CSV
- [ ] Deploy backend to Render.com
- [ ] Deploy frontend to Streamlit Cloud

---

## Data Sources & Credits

- **[OpenStreetMap](https://www.openstreetmap.org/)** — Restaurant data © OpenStreetMap contributors (ODbL)
- **[Nominatim](https://nominatim.org/)** — Geocoding
- **[Overpass API](https://overpass-api.de/)** — OSM data querying
- **[OSRM](http://project-osrm.org/)** — Open Source Routing Machine

---

## Security Notes

- This project requires **no API keys** and **no `.env` file**
- There is nothing sensitive to protect
- Safe to push to GitHub as-is

---

*Built with FastAPI + Streamlit · Data © OpenStreetMap contributors*
