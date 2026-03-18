from flask import Flask, render_template, request
import database

app = Flask(__name__)


@app.route("/")
def index():
    projects = database.get_all_projects()
    return render_template("project_assignment.html", projects=projects)


@app.route("/submit_profile", methods=["POST"])
def submit_profile():


    full_name = request.form.get("full_name", "").strip()
    name_parts = full_name.split(" ", 1)
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name  = name_parts[1] if len(name_parts) > 1 else ""

    data = {
        "first_name":        first_name,
        "last_name":         last_name,
        "email":             request.form.get("email", "").strip(),
        "experience":        request.form.get("experience", ""),
        "tech_stack":        request.form.get("tech_stack", ""),
        "duration":          request.form.get("duration", ""),
        "additional_skills": request.form.get("additional_skills", "").strip(),
        "availability":      request.form.get("availability") == "yes",
        "projects":          request.form.getlist("projects")
    }

    errors = []

    if not data["first_name"]:
        errors.append("Full name is required.")
    if not data["email"]:
        errors.append("Email address is required.")
    if "@" not in data["email"] or "." not in data["email"]:
        errors.append("Please enter a valid email address.")
    if not data["experience"]:
        errors.append("Experience level is required.")
    if not data["tech_stack"]:
        errors.append("Primary technology stack is required.")
    if not data["projects"]:
        errors.append("Please select at least one project.")
    if not data["duration"]:
        errors.append("Preferred project duration is required.")
    if not data["availability"]:
        errors.append("You must confirm your availability.")

    projects = database.get_all_projects()

    if errors:
        return render_template("project_assignment.html",
            errors=errors,
            projects=projects,
            form_data=data
        )

    # INSERT OR UPDATE LOGIC
    existing = database.get_employee_by_email(data["email"])

    if existing:
        database.update_employee(data, existing["employee_id"])
        message = "✅ Profile updated successfully!"
    else:
        database.insert_employee(data)
        message = "✅ Profile saved successfully!"

    # Refresh data to show updated selections
    saved = database.get_employee_by_email(data["email"])
    saved_projects = database.get_employee_project_ids(saved["employee_id"])

    return render_template("project_assignment.html",
        projects=projects,
        form_data=saved,
        selected_projects=saved_projects,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True)