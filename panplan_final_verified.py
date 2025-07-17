
import streamlit as st
import json
import os
import re

# ---------- Persistent User Storage ----------
USER_FILE = "users.json"
if os.path.exists(USER_FILE):
    with open(USER_FILE, "r") as f:
        user_db = json.load(f)
else:
    user_db = {}

def save_users():
    with open(USER_FILE, "w") as f:
        json.dump(user_db, f)

# ---------- Persistent Ratings Storage ----------
RATINGS_FILE = "ratings.json"
if os.path.exists(RATINGS_FILE):
    with open(RATINGS_FILE, "r") as rf:
        ratings_db = json.load(rf)
else:
    ratings_db = {}

def save_ratings():
    with open(RATINGS_FILE, "w") as rf:
        json.dump(ratings_db, rf)

# ---------- Streamlit Setup ----------
st.set_page_config(page_title="PanPlan", page_icon="🍲", layout="centered")
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&display=swap');
:root { color-scheme: light !important; }
html, body, [class*="css"] {
  font-family: 'Fredoka', sans-serif;
  background-color: #CDE5FA !important;
}
h1, h2, h3 { color: #3B5998; }
.stButton>button {
  background-color: #6B8ED6;
  color: white;
  border-radius: 10px;
  padding: 0.5em 1em;
  font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "view_recipe" not in st.session_state:
    st.session_state.view_recipe = None

# ---------- Login / Sign Up ----------
if not st.session_state.logged_in:
    st.image("PanPlan.png", width=100)
    st.title("Welcome to PanPlan")
    option = st.radio("Login or Sign Up", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if option == "Sign Up":
        name = st.text_input("Your Name")
    if st.button("Submit"):
        if option == "Login":
            if email in user_db and user_db[email]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.session_state.user_name = user_db[email]["name"]
                st.rerun()
            else:
                st.error("Invalid login.")
        else:
            if email in user_db:
                st.error("Email already registered.")
            else:
                user_db[email] = {"name": name, "password": password, "favorites": [], "votes": {}}
                save_users()
                st.success("Account created! Please log in.")
    st.stop()

# ---------- Preferences ----------
st.image("PanPlan.png", width=100)
st.title(f"Welcome, {user_db[st.session_state.user_email]['name']}!")
col1, col2 = st.columns(2)
preferences = []
if col1.checkbox("Vegan"): preferences.append("Vegan")
if col1.checkbox("Vegetarian"): preferences.append("Vegetarian")
if col2.checkbox("Gluten Free"): preferences.append("Gluten Free")
if col2.checkbox("Dairy Free"): preferences.append("Dairy Free")

# ---------- Substitution Data ----------
banned_ingredients = {
    "Vegan": {"Milk", "Eggs", "Butter", "Cream", "Chicken", "Beef", "Tuna", "Yogurt", "Cheese"},
    "Vegetarian": {"Chicken", "Beef", "Tuna"},
    "Gluten Free": {"Flour", "Pasta", "Bread", "Noodles"},
    "Dairy Free": {"Milk", "Butter", "Cream", "Yogurt", "Cheese"}
}
substitutions = {
    "Milk": "oat or almond milk", "Butter": "coconut oil", "Cream": "cauliflower cream",
    "Flour": "almond or oat flour", "Pasta": "gluten-free pasta", "Bread": "gluten-free bread",
    "Noodles": "rice noodles", "Yogurt": "plant-based yogurt", "Cheese": "nut-based cheese",
    "Chicken": "tofu or soy protein", "Beef": "lentils or mushrooms", "Tuna": "chickpeas"
}

recipes = {}  # placeholder; full recipe block will be inserted separately


recipes = {
    "Spaghetti with Tomato Sauce": {
        "category": "Pasta",
        "ingredients": ["200g Pasta", "1 tbsp Olive Oil", "2 cloves Garlic", "1 can Crushed Tomatoes", "Salt", "Pepper"],
        "instructions": ["Boil pasta until al dente.", "Sauté garlic in olive oil.", "Add tomatoes, salt, pepper. Simmer 10 minutes.", "Mix pasta with sauce and serve."]
    },
    "Creamy Chicken Pasta": {
        "category": "Pasta",
        "ingredients": ["200g Pasta", "1 Chicken Breast", "1/2 cup Cream", "1 tbsp Butter", "Salt", "Pepper"],
        "instructions": ["Cook pasta until al dente.", "Sauté chicken in butter until cooked.", "Add cream, simmer 5 mins.", "Combine with pasta and serve."]
    },
    "Vegetable Stir Fry": {
        "category": "Asian",
        "ingredients": ["1 Carrot", "1 Bell Pepper", "1 Zucchini", "2 tbsp Soy Sauce", "1 tsp Ginger", "1 tbsp Olive Oil"],
        "instructions": ["Slice all vegetables.", "Stir fry in olive oil.", "Add soy sauce and ginger. Serve hot."]
    },
    "Egg Fried Rice": {
        "category": "Asian",
        "ingredients": ["2 Eggs", "1 cup Rice", "2 tbsp Soy Sauce", "1/2 cup Peas", "1 tbsp Oil"],
        "instructions": ["Scramble eggs and set aside.", "Sauté rice and peas.", "Add eggs and soy sauce. Mix well."]
    },
    "Tuna Sandwich": {
        "category": "Sandwiches",
        "ingredients": ["2 slices Bread", "1 can Tuna", "1 tbsp Mayo", "Lettuce", "Salt", "Pepper"],
        "instructions": ["Mix tuna with mayo, salt, pepper.", "Spread on bread with lettuce.", "Close sandwich and serve."]
    },
    "Chickpea Salad": {
        "category": "Salads",
        "ingredients": ["1 can Chickpeas", "1/2 Cucumber", "10 Cherry Tomatoes", "Lemon Juice", "Salt", "Olive Oil"],
        "instructions": ["Combine chopped vegetables with chickpeas.", "Dress with lemon juice, salt, olive oil."]
    },
    "Beef Stir Fry": {
        "category": "Asian",
        "ingredients": ["100g Beef", "1 Bell Pepper", "1 tbsp Soy Sauce", "1 tsp Garlic", "1 tbsp Oil"],
        "instructions": ["Sauté beef until brown.", "Add pepper, soy sauce, garlic.", "Cook until tender."]
    },
    "Lentil Soup": {
        "category": "Soups",
        "ingredients": ["1 cup Lentils", "1 Carrot", "1 Celery stalk", "1 Onion", "4 cups Veg Broth", "1 tbsp Olive Oil"],
        "instructions": ["Sauté vegetables in oil.", "Add lentils and broth. Simmer 30 mins."]
    },
    "Greek Yogurt Parfait": {
        "category": "Breakfast",
        "ingredients": ["1 cup Yogurt", "1/2 cup Granola", "1/2 cup Berries"],
        "instructions": ["Layer yogurt, granola, and berries.", "Serve chilled."]
    },
    "Grilled Cheese": {
        "category": "Sandwiches",
        "ingredients": ["2 slices Bread", "2 slices Cheese", "1 tbsp Butter"],
        "instructions": ["Butter the bread slices.", "Place cheese between slices and grill until golden."]
    },
    "Caprese Salad": {
        "category": "Salads",
        "ingredients": ["Tomato", "Mozzarella", "Basil", "Olive Oil", "Salt"],
        "instructions": ["Slice tomatoes and mozzarella.", "Layer with basil, drizzle with oil and salt."]
    },
    "Veggie Tacos": {
        "category": "Mexican",
        "ingredients": ["Taco Shells", "1 Zucchini", "1/2 Onion", "1 Bell Pepper", "1 tbsp Olive Oil", "Salt"],
        "instructions": ["Sauté vegetables in oil.", "Fill taco shells and serve."]
    },
    "Mac and Cheese": {
        "category": "Pasta",
        "ingredients": ["200g Pasta", "1 cup Cheese", "1/2 cup Milk", "1 tbsp Butter"],
        "instructions": ["Cook pasta. Melt cheese with milk and butter.", "Mix with pasta and serve."]
    },
    "Stuffed Peppers": {
        "category": "Main Dishes",
        "ingredients": ["2 Bell Peppers", "1 cup Rice", "1/2 Onion", "1 tbsp Olive Oil", "Salt"],
        "instructions": ["Sauté onion and rice.", "Stuff into halved peppers. Bake until soft."]
    },
    "Yogurt Chicken Curry": {
        "category": "Indian",
        "ingredients": ["1 Chicken Breast", "1/2 cup Yogurt", "1 tsp Curry Powder", "1 tbsp Oil", "Salt"],
        "instructions": ["Marinate chicken in yogurt, curry powder, salt.", "Cook in oil until done."]
    }
}


# ---------- Substitution Function ----------
def apply_subs(ingredients, steps):
    banned = set()
    for pref in preferences:
        banned.update(banned_ingredients.get(pref, set()))
    updated_ingredients, subs = [], {}

    for ing in ingredients:
        egg_match = re.match(r"(\d+)\s*Eggs?", ing, re.IGNORECASE)
        if "Eggs" in banned and egg_match:
            qty = int(egg_match.group(1))
            sub_text = f"{qty * 60}mL commercial egg substitute"
            updated_ingredients.append(sub_text)
            subs["Eggs"] = sub_text
            continue
        updated = ing
        for b in sorted(banned, key=len, reverse=True):
            pattern = re.compile(rf"\b{b}\b", flags=re.IGNORECASE)
            if pattern.search(updated):
                updated = pattern.sub(substitutions[b], updated)
                subs[b] = substitutions[b]
        updated_ingredients.append(updated)

    updated_steps = []
    for step in steps:
        for b, s in subs.items():
            if re.match(rf"^{b}\b", step.strip(), re.IGNORECASE):
                continue
            step = re.sub(rf"\b{b}\b", s, step, flags=re.IGNORECASE)
        updated_steps.append(step)

    return updated_ingredients, updated_steps

# ---------- Recipe View ----------
view = st.session_state.view_recipe
email = st.session_state.user_email
user = user_db[email]
favs = set(user.get("favorites", []))
votes = user.get("votes", {})

if view:
    recipe = recipes[view]
    st.subheader(view)
    if st.button("❤️ Favorite" if view not in favs else "💔 Unfavorite"):
        if view in favs:
            favs.remove(view)
        else:
            favs.add(view)
        user["favorites"] = list(favs)
        save_users()
        st.rerun()

    ing, steps = apply_subs(recipe["ingredients"], recipe["instructions"])
    st.markdown("### Ingredients:")
    for i in ing:
        st.markdown(f"- {i}")
    st.markdown("### Instructions:")
    for i, s in enumerate(steps, 1):
        st.markdown(f"{i}. {s}")

    st.markdown("### Rate This Recipe")
    if view not in ratings_db:
        ratings_db[view] = {"likes": 0, "dislikes": 0}
    if view not in votes:
        votes[view] = None
    col1, col2 = st.columns(2)
    if col1.button("👍 Like"):
        if votes[view] != "like":
            if votes[view] == "dislike":
                ratings_db[view]["dislikes"] -= 1
            ratings_db[view]["likes"] += 1
            votes[view] = "like"
            user["votes"] = votes
            save_users()
            save_ratings()
            st.rerun()
    if col2.button("👎 Dislike"):
        if votes[view] != "dislike":
            if votes[view] == "like":
                ratings_db[view]["likes"] -= 1
            ratings_db[view]["dislikes"] += 1
            votes[view] = "dislike"
            user["votes"] = votes
            save_users()
            save_ratings()
            st.rerun()

    st.caption(f"👍 {ratings_db[view]['likes']}   👎 {ratings_db[view]['dislikes']}")

    if st.button("🔙 Go Back"):
        st.session_state.view_recipe = None
        st.rerun()

# ---------- Main Recipe Selection ----------
else:
    st.markdown("### ❤️ Your Favorite Recipes")
    for name in sorted(favs):
        if st.button(name, key="fav_" + name):
            st.session_state.view_recipe = name
            st.rerun()

    st.markdown("### All Recipes by Category")
    for cat in sorted(set(r["category"] for r in recipes.values())):
        with st.expander(cat):
            for name, r in recipes.items():
                if r["category"] == cat:
                    if st.button(name, key="btn_" + name):
                        st.session_state.view_recipe = name
                        st.rerun()
