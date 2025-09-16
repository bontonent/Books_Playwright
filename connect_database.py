# If you would like see what the DB I use
# ./SQL_script/books.sql

import psycopg2
import os

def connect_to_db():
    # Connect DB
    conn = psycopg2.connect(
        dbname = "books",
        user = "postgres",
        password = os.getenv('db_password'),
        port = os.getenv('db_port'),
        host = os.getenv('db_host')
    )
    cur = conn.cursor()

    # Return instrument DB
    return conn, cur

# Create new row in DB
def create_row(title, product_type, genre, price, stock, stars, upc,
               price_excl_tax, price_incl_tax, tax, number_of_reviews, img_url, describe):
    # Connect to DB
    conn, cur = connect_to_db()

    # Script
    cur.execute(
        "INSERT INTO products (title, product_type, genre, price, stock, stars, upc, "
        "price_excl_tax, price_incl_tax, tax, number_of_reviews, img_url, describe) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (title, product_type, genre, price, stock, stars, upc,
         price_excl_tax, price_incl_tax, tax, number_of_reviews, img_url, describe)
    )
    conn.commit()
    # Close connection (recommended)
    cur.close()
    conn.close()


    # Close DB
    cur.close()



