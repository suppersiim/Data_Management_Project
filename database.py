import psycopg2
from psycopg2.extras import RealDictCursor

# CONNECTION SETUP
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="employee_projects_db",
        user="postgres",
        password="postgres" 
    )



def get_all_projects():
    """Fetch all projects from DB to populate the dropdown."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT project_id, project_name FROM projects ORDER BY project_id")
    projects = cur.fetchall()
    cur.close()
    conn.close()
    return projects



def get_employee_by_email(email):
    """Find an employee by email — used to detect new vs returning user."""
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM employees WHERE email_address = %s", (email,))
    employee = cur.fetchone()
    cur.close()
    conn.close()
    return employee


def get_employee_project_ids(employee_id):
    """Get list of project IDs selected by an employee."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT project_id FROM employee_projects WHERE employee_id = %s",
        (employee_id,)
    )
    ids = [str(row[0]) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return ids


def insert_employee(data):
    """Insert a brand new employee and their project selections."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO employees 
            (first_name, last_name, email_address, experience_level,
             primary_technology_stack, preferred_project_duration,
             additional_skills, confirmed_availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING employee_id
    """, (
        data['first_name'],
        data['last_name'],
        data['email'],
        data['experience'],
        data['tech_stack'],
        data['duration'],
        data['additional_skills'],
        data['availability']
    ))

    employee_id = cur.fetchone()[0]
    _save_employee_projects(cur, employee_id, data['projects'])

    conn.commit()
    cur.close()
    conn.close()
    return employee_id


def update_employee(data, employee_id):
    """Update an existing employee's profile and project selections."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees SET
            first_name = %s,
            last_name = %s,
            experience_level = %s,
            primary_technology_stack = %s,
            preferred_project_duration = %s,
            additional_skills = %s,
            confirmed_availability = %s
        WHERE employee_id = %s
    """, (
        data['first_name'],
        data['last_name'],
        data['experience'],
        data['tech_stack'],
        data['duration'],
        data['additional_skills'],
        data['availability'],
        employee_id
    ))

    # Delete old project links and re-insert new ones
    cur.execute("DELETE FROM employee_projects WHERE employee_id = %s", (employee_id,))
    _save_employee_projects(cur, employee_id, data['projects'])

    conn.commit()
    cur.close()
    conn.close()


def _save_employee_projects(cur, employee_id, project_ids):
    """Link selected projects to an employee in the junction table."""
    for project_id in project_ids:
        cur.execute("""
            INSERT INTO employee_projects (employee_id, project_id)
            VALUES (%s, %s)
        """, (employee_id, project_id))

