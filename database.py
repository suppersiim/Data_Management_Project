import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "port": 5432
}


def create_database():
    # Connect to PostgreSQL with the 'postgres' database
    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = True
    cursor = conn.cursor()

    # Create the database if it doesn't exist
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'employee_projects';")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("CREATE DATABASE employee_projects;")
        print("Database 'employee_projects' created successfully.")
    else:
        print("Database 'employee_projects' already exists.")

    cursor.close()
    conn.close()



def create_tables():
    # Connect to PostgreSQL
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # Create employees table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id SERIAL PRIMARY KEY UNIQUE,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email_address TEXT NOT NULL UNIQUE,
            experience_level TEXT NOT NULL,
            primary_technology_stack TEXT NOT NULL,
            preferred_project_duration TEXT NOT NULL,
            additional_skills TEXT NOT NULL,
            confirmed_availability BOOLEAN NOT NULL
        );
    """)

    # Create projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id SERIAL PRIMARY KEY,
            project_name TEXT NOT NULL,
            project_duration TEXT NOT NULL,
            project_technology_stack TEXT NOT NULL,
            project_capacity INT NOT NULL,
            project_availability BOOLEAN NOT NULL
        );
    """)

    # Employee-project association table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_projects (
            employee_id INT REFERENCES employees(employee_id),
            project_id INT REFERENCES projects(project_id),
            PRIMARY KEY (employee_id, project_id)
        );
    """)

    # Commit changes and close connection
    conn.commit()
    cursor.close()
    conn.close()



def insert_employee(first_name, last_name, email, experience_level, primary_technology_stack, 
                    preferred_project_duration, additional_skills, confirmed_availability):
        
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Insert employee data into the employees table
    query = """
        INSERT INTO employees (first_name, last_name, email_address, experience_level, 
                                primary_technology_stack, preferred_project_duration, 
                                additional_skills, confirmed_availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING employee_id;
    """
    
    # Employee unique id
    employee_id = cursor.fetchone()[0]
    
    # Commit and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    
    return employee_id


def insert_project(project_name, project_duration, project_technology_stack, project_capacity, project_availability):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Insert project data into the projects table
    query = """
        INSERT INTO projects (project_name, project_duration, project_technology_stack, 
                                project_capacity, project_availability)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING project_id;
    """
    
    # Project unique id
    project_id = cursor.fetchone()[0]
    
    # Commit and close the connection
    connection.commit()
    cursor.close()
    connection.close()
    
    return project_id

def assign_employee_to_project(employee_id, project_id):
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()

    # Insert association data into the employee_projects table
    query = """
        INSERT INTO employee_projects (employee_id, project_id)
        VALUES (%s, %s);
    """
    
    cursor.execute(query, (employee_id, project_id))
    
    # Commit and close the connection
    connection.commit()
    cursor.close()
    connection.close()


create_database()
create_tables()


