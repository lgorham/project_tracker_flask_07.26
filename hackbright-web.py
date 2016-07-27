from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route("/")
def directory_homepage():
    """Show directory of all students and all projects"""

    student_list = hackbright.get_student_body()
    project_list = hackbright.get_all_projects()

    return render_template("homepage.html",
                            students=student_list,
                            projects=project_list)

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github','jhacks')
    first, last, github = hackbright.get_student_by_github(github)
    project_information = hackbright.get_grades_by_github(github)
    # return "%s is the GitHub account for %s %s" % (github, first, last)
    return render_template("student_info.html",
                            github=github, 
                            first=first, 
                            last=last,
                            project_information=project_information)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student"""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add():
    """Add a student."""

    return render_template("new_student.html")


@app.route("/add-to-database", methods=['POST'])
def add_database():
    """Add a student."""

    github_input = request.form.get('github')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    hackbright.make_new_student(first_name,last_name,github_input)

    return redirect("/student-search")



@app.route("/project")
def describe_project():
    """Gives title, description, and maximum grade of a project"""

    title = request.args.get('name')
    project_info = hackbright.get_project_by_title(title)
    project_title, description, max_grade = project_info

    project_grades = hackbright.get_grades_by_title(title)
    


    return render_template("/projects.html", 
                            project_title=project_title, 
                            description=description,
                            max_grade=max_grade,
                            grades=project_grades)


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
