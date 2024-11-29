import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

# Function to connect to MySQL server
def connect_to_server():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("USER"),  # Replace with your MySQL username
            password=os.getenv("PASSWORD")  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None


# Function to connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            database=os.getenv("DBNAME"),
            user=os.getenv("USER"),  # Replace with your MySQL username
            password=os.getenv("PASSWORD")  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
    return None

# Function to initialize database and table
def initialize_database_and_table():
    connection = connect_to_server()
    if not connection:
        print("Failed to connect to MySQL server.")
        return

    try:
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS ProblemHistoryDB;")

        # Use the database
        cursor.execute("USE ProblemHistoryDB;")

        # Create table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS EloRatings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {", ".join([f"dimension{i+1}_elo FLOAT NOT NULL" for i in range(115)])}
        );
        """
        cursor.execute(create_table_query)
        print("Database and table initialized successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to add a new row to the EloRatings table
def add_elo_entry(dimension_elos):
    connection = connect_to_db()
    if not connection:
        print("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()

        # Prepare the query to insert values
        placeholders = ', '.join(['%s'] * 115)
        query = f"""
        INSERT INTO EloRatings (
            {', '.join([f'dimension{i+1}_elo' for i in range(115)])}
        ) VALUES ({placeholders});
        """
        cursor.execute(query, dimension_elos)
        connection.commit()
        print("Elo entry added successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Function to get the latest row from the EloRatings table
def get_latest_elo_entry():
    connection = connect_to_db()
    if not connection:
        print("Failed to connect to the database.")
        return [0.0] * 115  # Return all zeros if connection fails

    try:
        cursor = connection.cursor()

        # Query to get the latest row by id
        query = f"""
        SELECT {', '.join([f'dimension{i+1}_elo' for i in range(115)])}
        FROM EloRatings
        ORDER BY id DESC LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        # If table is empty, insert and return a row with all zeros
        if not result:
            print("Table is empty. Initializing with all zeros.")
            zero_row = [0.0] * 115
            add_elo_entry(zero_row)
            return zero_row
        else:
            return list(result)
    except Error as e:
        print(f"Error: {e}")
        return [0.0] * 115  # Return all zeros if there's an error
    finally:
        cursor.close()
        connection.close()

# Example Usage
# if __name__ == "__main__":
#     # Initialize the database and table
#     initialize_database_and_table()

#     # Add a new Elo entry
#     dimension_elos = [1200 + i for i in range(115)]  # Example Elo values
#     add_elo_entry(dimension_elos)

#     # Get the latest Elo entry
#     latest_elo_entry = get_latest_elo_entry()
#     print("Latest Elo Ratings:", latest_elo_entry)
