import os
from dotenv import load_dotenv

# Only load .env file if NOT running inside Docker
if not os.environ.get("DB_HOST"):
    load_dotenv()

DB_HOST     = os.environ.get("DB_HOST", "localhost")
DB_NAME     = os.environ.get("DB_NAME", "employee_projects_db")
DB_USER     = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "postgres")