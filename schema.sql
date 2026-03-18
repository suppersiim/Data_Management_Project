
/*CREATE EMPLOYEES TABLE*/
CREATE TABLE IF NOT EXISTS employees (
            employee_id SERIAL PRIMARY KEY ,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email_address TEXT NOT NULL UNIQUE,
            experience_level TEXT NOT NULL,
            primary_technology_stack TEXT NOT NULL,
            preferred_project_duration TEXT NOT NULL,
            additional_skills TEXT,
            confirmed_availability BOOLEAN NOT NULL
        );

/*CREATE PROJECTS TABLE*/
CREATE TABLE IF NOT EXISTS projects (
            project_id SERIAL PRIMARY KEY,
            project_name TEXT NOT NULL,
            project_duration TEXT NOT NULL,
            project_technology_stack TEXT NOT NULL,
            project_capacity INT NOT NULL,
            project_availability BOOLEAN NOT NULL
        );



/*CREATE EMPLOYEE-PROJECTS RELATIONSHIP TABLE*/
CREATE TABLE IF NOT EXISTS employee_projects (
            employee_id INT REFERENCES employees(employee_id) ON DELETE CASCADE,
            project_id INT REFERENCES projects(project_id) ON DELETE CASCADE,
            PRIMARY KEY (employee_id, project_id)
        );


/* INSERT 10 RANDOM PROJECTS */
INSERT INTO projects (project_name, project_duration, project_technology_stack, project_capacity, project_availability) VALUES
    ('Customer Portal Redesign',             'medium', 'frontend',  5, TRUE),
    ('Data Pipeline Migration',              'long',   'data',      3, TRUE),
    ('Mobile App Enhancement',               'short',  'mobile',    4, TRUE),
    ('Internal Analytics Dashboard',         'medium', 'data',      4, TRUE),
    ('API Gateway Implementation',           'medium', 'backend',   3, TRUE),
    ('Cloud Infrastructure Setup',           'long',   'devops',    2, TRUE),
    ('E-commerce Platform Update',           'medium', 'fullstack', 6, TRUE),
    ('Reporting System Automation',          'short',  'backend',   4, TRUE),
    ('Microservices Architecture Transition','long',   'backend',   3, TRUE),
    ('Customer Data Platform Integration',   'long',   'data',      4, TRUE)
ON CONFLICT DO NOTHING;