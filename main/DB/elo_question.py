import mysql.connector
from mysql.connector import Error

# Connect to MySQL server
def connect_to_server():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Replace with your MySQL username
            password='yourpassword'  # Replace with your MySQL password
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Connect to the database
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ProblemHistoryDB',
            user='root',
            password='yourpassword'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Ensure the database and table exist
def initialize_database_and_table():
    connection = connect_to_server()
    if not connection:
        print("Connection to MySQL server failed.")
        return

    try:
        cursor = connection.cursor()

        # Create database if it doesn't exist
        cursor.execute("CREATE DATABASE IF NOT EXISTS ProblemHistoryDB;")

        # Use the database
        cursor.execute("USE ProblemHistoryDB;")

        # Create table if it doesn't exist
        create_table_query = """
        CREATE TABLE IF NOT EXISTS EloRatings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            cumulative_elo FLOAT NOT NULL,
            """ + ", ".join([f"dimension{i+1}_elo FLOAT NOT NULL" for i in range(115)]) + """
        );
        """
        cursor.execute(create_table_query)
        print("Database and table initialized successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Add an Elo entry to the table
def add_elo_entry(cumulative_elo, dimension_elos):
    connection = connect_to_db()
    if not connection:
        print("Connection failed.")
        return

    try:
        cursor = connection.cursor()
        dimension_elo_values = ', '.join(['%s'] * 115)
        query = f"""
        INSERT INTO EloRatings (
            cumulative_elo, {', '.join([f'dimension{i+1}_elo' for i in range(115)])}
        ) VALUES (%s, {dimension_elo_values});
        """
        cursor.execute(query, [cumulative_elo] + dimension_elos)
        connection.commit()
        print("Elo entry added successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        connection.close()

# Get the latest Elo entry
def get_latest_elo_entry():
    connection = connect_to_db()
    if not connection:
        print("Connection failed.")
        return {"cumulative_elo": 0.0, "dimension_elos": [0.0] * 115}  # Return all zeros if connection fails

    try:
        cursor = connection.cursor()
        query = f"""
        SELECT cumulative_elo, {', '.join([f'dimension{i+1}_elo' for i in range(115)])}
        FROM EloRatings ORDER BY id DESC LIMIT 1;
        """
        cursor.execute(query)
        result = cursor.fetchone()

        # If the table is empty, return all zeros
        if not result:
            print("Table is empty. Returning all zeros.")
            return {"cumulative_elo": 0.0, "dimension_elos": [0.0] * 115}
        else:
            return {"cumulative_elo": result[0], "dimension_elos": result[1:]}
    except Error as e:
        print(f"Error: {e}")
        return {"cumulative_elo": 0.0, "dimension_elos": [0.0] * 115}  # Return all zeros if there's an error
    finally:
        cursor.close()
        connection.close()

# Check if the table is empty and initialize with zeros if necessary

# Example Usage
if __name__ == "__main__":
    # Ensure database and table exist
    initialize_database_and_table()


    # Add a new Elo entry
    cumulative_elo = 1300.0  # Example cumulative Elo
    dimension_elos = [1200 + i for i in range(115)]  # Replace with actual Elo values
    add_elo_entry(cumulative_elo, dimension_elos)

    # Get the latest Elo entry
    latest_entry = get_latest_elo_entry()
    if latest_entry:
        print(f"Latest Cumulative Elo: {latest_entry['cumulative_elo']}")
        print(f"Latest Elo Ratings for Dimensions: {latest_entry['dimension_elos']}")
    else:
        print("No Elo ratings found.")
