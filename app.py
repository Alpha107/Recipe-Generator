import streamlit as st
import requests

# ----------------------------
# API SETTINGS (Spoonacular)
# ----------------------------
SEARCH_URL = "https://api.spoonacular.com/recipes/complexSearch"
INFO_URL   = "https://api.spoonacular.com/recipes/{id}/information"
API_KEY    = "Your API Key"

# ----------------------------
# PAGE CONFIG & STYLING
# ----------------------------
st.set_page_config(
    page_title="🍲 Recipe Generator",
    page_icon="🥣",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main { background-color: #FAFAFA; }
    .title {
        font-size: 2.4rem;
        font-weight: 700;
        color: #4B4B4B;
    }
    .subheader { color: #6F6F6F; }
    .footer { font-size: 0.75rem; color: #A0A0A0; }

    /* Metric card styling */
    [data-testid="stMetric"] {
        background-color: #F0F4FF;
        border: 1px solid #D6E0FF;
        border-radius: 10px;
        padding: 12px 16px;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
        color: #555;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.3rem;
        font-weight: 700;
        color: #2C3E50;
    }
</style>
""", unsafe_allow_html=True)

# ----------------------------
# SIDEBAR
# ----------------------------
st.sidebar.title("🎯 Enter Your Query")
dish = st.sidebar.text_input(
    "What recipe do you want?",
    help="Example: lentil soup, chocolate cake, spaghetti"
)
desired_servings = st.sidebar.number_input(
    "🍽️ Number of Servings",
    min_value=1,
    max_value=50,
    value=1,
    step=1,
    help="Adjust to scale ingredient quantities and nutrition automatically"
)
st.sidebar.button("Generate Recipe")

# ----------------------------
# MAIN HEADER
# ----------------------------
st.markdown("<h1 class='title'>🍽️ Recipe Generator</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Get instant recipes with full nutrition info powered by Spoonacular.</p>", unsafe_allow_html=True)
st.write("---")

# ----------------------------
# HELPER: find a nutrient value by name from nutrition.nutrients list
# ----------------------------
def get_nutrient(nutrients, name):
    """Return the amount of a nutrient by name, or None if not found."""
    for n in nutrients:
        if n.get("name", "").lower() == name.lower():
            return n.get("amount")
    return None

# ----------------------------
# GET RECIPE
# ----------------------------
if dish:
    with st.spinner(f"🔎 Searching for '{dish}'..."):
        try:
            # Step 1: Search for the recipe to get its ID
            search_resp = requests.get(SEARCH_URL, params={
                "query": dish,
                "number": 1,
                "apiKey": API_KEY
            })

            if search_resp.status_code != 200:
                st.error(f"⚠️ Search API Error: {search_resp.status_code} — {search_resp.text}")
            else:
                search_data = search_resp.json()
                results = search_data.get("results", [])

                if not results:
                    st.warning("😕 No recipe found. Try another dish name!")
                else:
                    recipe_id = results[0]["id"]

                    # Step 2: Get full recipe details including nutrition
                    info_resp = requests.get(
                        INFO_URL.format(id=recipe_id),
                        params={
                            "includeNutrition": "true",
                            "apiKey": API_KEY
                        }
                    )

                    if info_resp.status_code != 200:
                        st.error(f"⚠️ Recipe Info API Error: {info_resp.status_code}")
                    else:
                        recipe = info_resp.json()

                        # --- Servings scaling ---
                        original_servings = recipe.get("servings", 1) or 1
                        try:
                            original_servings = float(original_servings)
                        except (ValueError, TypeError):
                            original_servings = 1.0
                        scale = desired_servings / original_servings if original_servings > 0 else 1.0

                        # --- Recipe title & image ---
                        st.subheader(f"📌 {recipe.get('title', 'Unknown').title()}")
                        image_url = recipe.get("image")
                        if image_url:
                            st.image(image_url, use_container_width=True)

                        # --- Helpers ---
                        def scale_val(val):
                            try:
                                return round(float(val) * scale, 2) if val is not None else None
                            except (ValueError, TypeError):
                                return None

                        def fmt(val, suffix=""):
                            return f"{val}{suffix}" if val is not None else "N/A"

                        # --- Summary section ---
                        summary = recipe.get("summary", "")
                        if summary:
                            import re
                            clean_summary = re.sub(r"<[^>]+>", "", summary)
                            st.markdown(f"*{clean_summary}*")
                        
                        # --- Dietary Badges ---
                        badges = []
                        if recipe.get("vegetarian"): badges.append("🥗 Vegetarian")
                        if recipe.get("vegan"):      badges.append("🌱 Vegan")
                        if recipe.get("glutenFree"): badges.append("🌾 Gluten-Free")
                        if recipe.get("dairyFree"):  badges.append("🥛 Dairy-Free")
                        if recipe.get("veryHealthy"): badges.append("💪 Very Healthy")

                        if badges:
                            st.write("  ·  ".join(badges))
                        st.write("")

                        # --- Details section ---
                        st.markdown("### 📊 Details")
                        ready_raw = recipe.get("readyInMinutes")
                        ready_val = f"{ready_raw} min" if ready_raw else "N/A"

                        NPR_RATE = 140  # Rs. 140 = $1
                        price_usd = recipe.get('pricePerServing', 0)
                        if price_usd:
                            price_usd_val = price_usd / 100
                            price_npr_val = price_usd_val * NPR_RATE
                            price_display     = f"${price_usd_val:.2f}"
                            price_npr_display = f"approx Rs. {price_npr_val:.0f}"
                        else:
                            price_display     = "N/A"
                            price_npr_display = "N/A"

                        d1, d2, d3 = st.columns(3)
                        d1.metric("🍽️ Servings",    desired_servings)
                        d2.metric("⏱️ Ready In",     ready_val)
                        
                        # Custom Price Card to balance font sizes
                        with d3:
                            st.markdown(f"""
                                <div style="background-color: #F0F4FF; border: 1px solid #D6E0FF; border-radius: 10px; padding: 12px 16px; height: 100%;">
                                    <div style="font-size: 0.8rem; color: #555; margin-bottom: 4px;">🇳🇵💰 Price/Serving</div>
                                    <div style="color: #2C3E50;">
                                        <span style="font-size: 1.25rem; font-weight: 700;">{price_display}</span>
                                        <span style="font-size: 0.85rem; color: #666; margin-left: 8px;">({price_npr_display})</span>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                        st.write("")

                        # --- Ingredients ---
                        st.markdown("### 🥕 Ingredients")
                        if scale != 1.0:
                            st.caption(f"📐 Scaled from {int(original_servings)} → {desired_servings} serving(s)")

                        ingredients = recipe.get("extendedIngredients", [])
                        if ingredients:
                            for item in ingredients:
                                name_i  = item.get("name", "Unknown").capitalize()
                                amount  = item.get("amount", "")
                                unit    = item.get("unit", "")
                                scaled  = fmt(scale_val(amount))
                                st.write(f"- **{name_i}** — {scaled} {unit}".strip())
                        else:
                            st.write("No ingredients available.")

                        # --- Instructions ---
                        st.markdown("### 📝 Instructions")
                        instructions = recipe.get("instructions", "")
                        if instructions:
                            import re
                            # Remove HTML tags
                            clean = re.sub(r"<[^>]+>", "", instructions)
                            # Split on numbered steps like "1.", "2.", etc.
                            steps = re.split(r"(?<!\d)(\d+)\.\s+", clean)
                            # re.split with a capturing group gives: ['', '1', 'text', '2', 'text', ...]
                            # Pair up the step numbers with their text
                            parsed = []
                            i = 1
                            while i < len(steps) - 1:
                                step_num  = steps[i].strip()
                                step_text = steps[i + 1].strip()
                                if step_text:
                                    parsed.append((step_num, step_text))
                                i += 2

                            if parsed:
                                for num, text in parsed:
                                    st.markdown(f"**Step {num}.** {text}")
                                    st.write("")
                            else:
                                # Fallback: just show the cleaned text
                                st.write(clean)
                        else:
                            st.write("No instructions available.")

                        # --- Nutrition ---
                        st.markdown("### 🍱 Nutrition Information")
                        if scale != 1.0:
                            st.caption(f"📐 Nutrition scaled for {desired_servings} serving(s)")

                        nutrition_obj  = recipe.get("nutrition", {})
                        nutrients_list = nutrition_obj.get("nutrients", [])

                        if nutrients_list:
                            calories = scale_val(get_nutrient(nutrients_list, "Calories"))
                            protein  = scale_val(get_nutrient(nutrients_list, "Protein"))
                            carbs    = scale_val(get_nutrient(nutrients_list, "Carbohydrates"))
                            fat      = scale_val(get_nutrient(nutrients_list, "Fat"))
                            sugar    = scale_val(get_nutrient(nutrients_list, "Sugar"))
                            fiber    = scale_val(get_nutrient(nutrients_list, "Fiber"))

                            n1, n2, n3 = st.columns(3)
                            n1.metric("🔥 Calories",  fmt(calories))
                            n2.metric("🥩 Protein",   fmt(protein,  " g"))
                            n3.metric("🍞 Carbs",     fmt(carbs,    " g"))

                            st.write("")
                            n4, n5, n6 = st.columns(3)
                            n4.metric("🧈 Fat",       fmt(fat,      " g"))
                            n5.metric("🍬 Sugar",     fmt(sugar,    " g"))
                            n6.metric("🌾 Fiber",     fmt(fiber,    " g"))
                        else:
                            st.info("ℹ️ Nutrition data not available for this recipe.")

        except requests.exceptions.RequestException as e:
            st.error(f"💥 Network Error: {e}")

else:
    st.info("🔎 Enter a dish name in the sidebar to generate a recipe.")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("<div class='footer'>Built by MeroCodingClass. Powered by Spoonacular API.</div>", unsafe_allow_html=True)
