import streamlit as st
import pandas as pd
from db import (
    get_food_listings,
    insert_food,
    get_filtered_food,
    get_providers,
    get_receivers,
    get_claims
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Food Wastage Management System",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("Food Wastage Management System")

# =========================
# CREATE – ADD FOOD
# =========================
st.subheader("Add Food Listing (CREATE)")

with st.form("add_food_form"):
    food_name = st.text_input("Food Name")
    food_type = st.selectbox(
        "Food Type",
        ["Veg", "Non-Veg", "Vegan", "Other"]
    )
    provider_type = st.selectbox(
        "Provider Type",
        ["GroceryStore", "Restaurant", "Supermarket", "Catering Service"]
    )
    quantity = st.number_input(
        "Quantity (servings)",
        min_value=1,
        step=1
    )
    location = st.text_input("Location")
    expiry_date = st.date_input("Expiry Date")
    contact = st.text_input("Contact Number / Email")

    submitted = st.form_submit_button("Add Food")

if submitted:
    if food_name == "" or location == "" or contact == "":
        st.error("Please fill all required fields")
    else:
        # Using a dummy provider_id (can be improved later)
        provider_id = 999

        insert_food(
            food_name=food_name,
            quantity=quantity,
            expiry_date=expiry_date,
            provider_id=provider_id,
            provider_type=provider_type,
            location=location,
            food_type=food_type
        )

        st.success("Food added successfully ✅")

# =========================
# READ – FOOD LISTINGS
# =========================
st.divider()
st.subheader("Available Food Listings (READ)")

food_df = get_food_listings()

if food_df.empty:
    st.info("No food listings available.")
else:
    st.dataframe(food_df, use_container_width=True)

# =========================
# FILTER FOOD
# =========================
st.subheader("Filter Food Listings")

col1, col2 = st.columns(2)

with col1:
    filter_location = st.text_input(
        "Filter by Location (type anything like 'mark')"
    )

with col2:
    filter_provider_type = st.selectbox(
        "Filter by Provider Type",
        ["All", "GroceryStore", "Restaurant", "Supermarket", "Catering Service"]
    )

filtered_df = get_filtered_food(
    location=filter_location if filter_location else None,
    provider_type=filter_provider_type
)

if filtered_df.empty:
    st.warning("No matching food listings found.")
else:
    st.dataframe(filtered_df, use_container_width=True)

# =========================
# PROVIDERS TABLE
# =========================
st.divider()
st.subheader("Providers")

providers_df = get_providers()
if providers_df.empty:
    st.info("No providers data available.")
else:
    st.dataframe(providers_df, use_container_width=True)

# =========================
# RECEIVERS TABLE
# =========================
st.divider()
st.subheader("Receivers")

receivers_df = get_receivers()
if receivers_df.empty:
    st.info("No receivers data available.")
else:
    st.dataframe(receivers_df, use_container_width=True)

# =========================
# CLAIMS TABLE
# =========================
st.divider()
st.subheader("Claims")

claims_df = get_claims()
if claims_df.empty:
    st.info("No claims data available.")
else:
    st.dataframe(claims_df, use_container_width=True)
