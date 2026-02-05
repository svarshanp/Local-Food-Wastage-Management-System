import sqlite3
import pandas as pd
import os

DB_NAME = "foodwaste.db"

DATA_FOLDER = "data"
PROVIDERS_CSV = os.path.join(DATA_FOLDER, "providers.csv")
RECEIVERS_CSV = os.path.join(DATA_FOLDER, "receivers.csv")
FOOD_LISTINGS_CSV = os.path.join(DATA_FOLDER, "food_listings.csv")
CLAIMS_CSV = os.path.join(DATA_FOLDER, "claims.csv")


def create_tables(conn):
    cursor = conn.cursor()

    # Providers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS providers (
        Provider_ID INTEGER PRIMARY KEY,
        Provider_Name TEXT,
        Provider_Type TEXT,
        Location TEXT,
        Contact TEXT
    )
    """)

    # Receivers
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS receivers (
        Receiver_ID INTEGER PRIMARY KEY,
        Receiver_Name TEXT,
        Receiver_Type TEXT,
        Location TEXT,
        Contact TEXT
    )
    """)

    # Food Listings
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS food_listings (
        Food_ID INTEGER PRIMARY KEY,
        Food_Name TEXT,
        Quantity INTEGER,
        Expiry_Date TEXT,
        Provider_ID INTEGER,
        Provider_Type TEXT,
        Location TEXT,
        Food_Type TEXT
    )
    """)

    # Claims
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        Claim_ID INTEGER PRIMARY KEY,
        Food_ID INTEGER,
        Receiver_ID INTEGER,
        Status TEXT,
        Timestamp TEXT
    )
    """)

    conn.commit()


def load_csv_to_db(conn, csv_path, table_name):
    df = pd.read_csv(csv_path)

    # remove old data every time you run init_db.py (so you don’t get duplicates)
    conn.execute(f"DELETE FROM {table_name}")
    conn.commit()

    df.to_sql(table_name, conn, if_exists="append", index=False)


def main():
    conn = sqlite3.connect(DB_NAME)

    create_tables(conn)

    load_csv_to_db(conn, PROVIDERS_CSV, "providers")
    load_csv_to_db(conn, RECEIVERS_CSV, "receivers")
    load_csv_to_db(conn, FOOD_LISTINGS_CSV, "food_listings")
    load_csv_to_db(conn, CLAIMS_CSV, "claims")

    conn.close()
    print("✅ Database created + CSV data inserted successfully!")


if __name__ == "__main__":
    main()
