# Telia Data Management — Project Assignment Application

A web application for managing internal project assignments built for the Telia Data Management Developer Internship home assignment.

Employees can register their profile, select projects they are interested in, and update their information as needed.


## Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Backend   | Python 3.11 / Flask     |
| Database  | PostgreSQL 15           |
| Frontend  | HTML, CSS, Jinja2       |
| Container | Docker & Docker Compose |

## Project Structure
```
Data_Management_Project/
├── Dockerfile                    # Docker image for Flask app
├── docker-compose.yml            # Runs Flask + PostgreSQL together
├── .dockerignore                 # Files excluded from Docker build
├── app.py                        # Flask application and routes
├── database.py                   # Database connection and queries
├── config.py                     # Configuration and environment variables
├── schema.sql                    # Database schema and seed data
├── database_dump.sql             # Full database dump (structure + data)
├── requirements.txt              # Python dependencies
├── .gitignore                    # Files excluded from Git
├── README.md                     # Project documentation
├── static/
│   └── style.css                 # Application styles
└── templates/
    └── project_assignment.html   # Frontend form template
```

## Features

- Register employee profile with experience level and technology stack
- Select one or more projects from a dynamically generated dropdown
- Automatically detects new vs returning user by email — performs INSERT or UPDATE accordingly
- After saving, the form is pre-filled with the saved data
- Client-side validation via HTML attributes
- Server-side validation with proper error messages
- Environment variables for secure database configuration
- Fully containerized with Docker — one command setup


## Database Schema

### employees
Stores employee profile information including name, email, experience level, technology stack, preferred project duration, additional skills, and availability confirmation.

### projects
Stores all available projects seeded from the original assignment HTML file. Contains project name, duration, technology stack, capacity, and availability.

### employee_projects
Junction table linking employees to their selected projects. Implements the many-to-many relationship between employees and projects with cascading deletes.

## Setup instructions

### Steps

**1. Clone the repository**
```bash
git clone 
cd Data_Management_Project
```

**2. Create a `.env` file in the project root**
```
DB_HOST=db
DB_NAME=employee_projects_db
DB_USER=postgres
DB_PASSWORD=postgres
```

**3. Start the application**
```bash
docker-compose up --build
```

**4. Open in browser**
```
http://127.0.0.1:5000
```

## Restore Database from Dump
```bash
psql -U postgres -d employee_projects_db -f database_dump.sql
```

## Validation Rules

- Full name is required
- Email address is required and must be in valid format
- Experience level is required
- Primary technology stack is required
- At least one project must be selected
- Preferred project duration is required
- Availability checkbox must be confirmed


## AI Assistance

This project was built using AI-assisted development (Claude by Anthropic) —
commonly referred to as "vibe coding". As someone newer to web development,
I used AI as a collaborative tool throughout the process rather than writing
every line of code from scratch myself.

What this means in practice:
- The code was written with AI assistance
- All architectural decisions were made collaboratively —
  PostgreSQL, Flask, Docker, schema design, validation logic
- I could not have built this without AI assistance, and I am not claiming otherwise

I believe AI-assisted development is a legitimate and increasingly important
skill in modern software engineering. The ability to direct AI effectively
and make good technical decisions is itself a valuable skill — and one I
practiced throughout this project.
