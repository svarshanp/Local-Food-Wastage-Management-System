import sqlite3
import pandas as pd

DB_NAME = "foodwaste.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


# ---------------- FOOD LISTINGS ----------------
def get_food_listings():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM food_listings", conn)
    conn.close()
    return df


def insert_food(food_name, quantity, expiry_date, provider_id, provider_type, location, food_type):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO food_listings (Food_Name, Quantity, Expiry_Date, Provider_ID, Provider_Type, Location, Food_Type)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (food_name, quantity, str(expiry_date), provider_id, provider_type, location, food_type))

    conn.commit()
    conn.close()


def get_filtered_food(location=None, provider_type=None):
    conn = get_connection()

    query = "SELECT * FROM food_listings WHERE 1=1"
    params = []

    if location:
        query += " AND LOWER(Location) LIKE ?"
        params.append(f"%{location.lower()}%")

    if provider_type and provider_type != "All":
        query += " AND Provider_Type = ?"
        params.append(provider_type)

    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df


# ---------------- PROVIDERS ----------------
def get_providers():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM providers", conn)
    conn.close()
    return df


# ---------------- RECEIVERS ----------------
def get_receivers():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM receivers", conn)
    conn.close()
    return df


# ---------------- CLAIMS ----------------
def get_claims():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM claims", conn)
    conn.close()
    return df
