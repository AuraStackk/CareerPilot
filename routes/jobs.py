from flask import Blueprint, render_template, request, redirect, session, flash
from models import db, Job, User
import os
from werkzeug.utils import secure_filename
import PyPDF2
from flask_login import  current_user
from datetime import datetime
import csv
from flask import make_response


jobs_bp = Blueprint("jobs", __name__)

# ---------------- DASHBOARD ----------------
@jobs_bp.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    search = request.args.get("search")
    status = request.args.get("status")
    location = request.args.get("location")
    work_type = request.args.get("work_type")

    jobs_query = Job.query.filter_by(user_id=user.id)

    # 🔍 SEARCH
    if search:
        jobs_query = jobs_query.filter(
            Job.company.ilike(f"%{search}%") |
            Job.role.ilike(f"%{search}%")
        )

    # 🎯 FILTERS
    if status:
        jobs_query = jobs_query.filter_by(status=status)

    if location:
        jobs_query = jobs_query.filter_by(location=location)

    if work_type:
        jobs_query = jobs_query.filter_by(work_type=work_type)

    jobs = jobs_query.order_by(
        Job.created_at.desc()
    ).all()

    # 💎 DASHBOARD COUNTERS
    total_jobs = Job.query.filter_by(
        user_id=user.id
    ).count()

    applied_jobs = Job.query.filter_by(
        user_id=user.id,
        status="Applied"
    ).count()

    interview_jobs = Job.query.filter_by(
        user_id=user.id,
        status="Interview"
    ).count()

    rejected_jobs = Job.query.filter_by(
        user_id=user.id,
        status="Rejected"
    ).count()

    # 📈 INTERVIEW RATE
    if total_jobs > 0:
        interview_rate = round(
            (interview_jobs / total_jobs) * 100
        )
    else:
        interview_rate = 0

    # 📊 REAL MONTHLY ANALYTICS
    months = []
    applications = []

    for month in range(1, 13):

        count = Job.query.filter(
            Job.user_id == user.id,
            db.extract('month', Job.created_at) == month
        ).count()

        month_name = datetime(
            2026,
            month,
            1
        ).strftime("%b")

        months.append(month_name)

        applications.append(count)

        # SMART INSIGHTS

    insights = []

    if applied_jobs >= 10:
     insights.append(
        "🔥 Great consistency! You're actively applying."
    )

    if interview_jobs >= 3:
     insights.append(
        "🎯 Interviews are increasing. Your resume is working."
    )

    if rejected_jobs >= 5:
     insights.append(
        "⚠️ High rejection rate. Improve resume/projects."
    )

    if total_jobs == 0:
     insights.append(
        "🚀 Start applying to track your career journey."
    )
     
    recent_jobs = Job.query.filter_by(
        user_id=user.id
    ).order_by(
        Job.created_at.desc()
    ).limit(5).all()

    monthly_goal = 20
    goal_progress = min(
    100,
    round((total_jobs / monthly_goal) * 100)
)
    resume_score = user.resume_score or "0%"

    if total_jobs == 0:
     dashboard_message = "Add your first application to start tracking."
    elif interview_rate >= 50:
     dashboard_message = "Great progress! Your interview rate is strong."
    else:
     dashboard_message = "Keep applying consistently to improve results."


    return render_template(
        "dashboard.html",
        username=user.username,
        jobs=jobs,
        total_jobs=total_jobs,
        applied_jobs=applied_jobs,
        interview_jobs=interview_jobs,
        rejected_jobs=rejected_jobs,
        interview_rate=interview_rate,
        months=months,
        applications=applications,
        insights=insights,
        recent_jobs=recent_jobs,
        monthly_goal=monthly_goal,
        goal_progress=goal_progress,
        resume_score=resume_score,
        dashboard_message=dashboard_message
    )

@jobs_bp.route("/job/<int:id>")
def job_detail(id):

    if "user_id" not in session:
        return redirect("/login")

    job = Job.query.get(id)

    if not job or job.user_id != session["user_id"]:
        return "Not found"

    return render_template("job_detail.html", job=job)


@jobs_bp.route("/export-csv")
def export_csv():

    if "user_id" not in session:
        return redirect("/login")

    jobs = Job.query.filter_by(
        user_id=session["user_id"]
    ).all()

    output = []

    output.append(
        "Company,Role,Status,Priority,Salary,Location,Work Type\n"
    )

    for job in jobs:

        output.append(
            f"{job.company},{job.role},{job.status},{job.priority},{job.salary},{job.location},{job.work_type}\n"
        )

    response = make_response(
        "".join(output)
    )

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=careerpilot_jobs.csv"

    response.headers[
        "Content-Type"
    ] = "text/csv"

    return response
    


# ---------------- ADD JOB ----------------
@jobs_bp.route("/add-job", methods=["GET", "POST"])
def add_job():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        status = request.form["status"]
        priority = request.form["priority"]
        salary = request.form["salary"]
        work_type = request.form["work_type"]
        location = request.form["location"]
        notes = request.form["notes"]

        new_job = Job(
            company=company,
            role=role,
            status=status,
            priority=priority,
            salary=salary,
            work_type=work_type,
            location=location,
            notes=notes,
            user_id=session["user_id"]
        )

        db.session.add(new_job)
        db.session.commit()

        flash("Job added successfully!")  # 💎 NEW

        return redirect("/dashboard")

    return render_template("add_job.html")


# ---------------- DELETE JOB ----------------
@jobs_bp.route("/delete-job/<int:id>", methods=["POST"])
def delete_job(id):
    if "user_id" not in session:
        return redirect("/login")

    job = Job.query.get(id)

    if not job:
     return "Job not found"

    if job.user_id != session["user_id"]:
        return "Unauthorized"

    db.session.delete(job)
    db.session.commit()

    flash("Job deleted successfully!")  # 💎 NEW

    return redirect("/dashboard")

# ---------------- UPDATE STATUS ----------------
@jobs_bp.route("/update-status/<int:id>", methods=["POST"])
def update_status(id):
    if "user_id" not in session:
        return redirect("/login")

    job = Job.query.get(id)

    # security check
    if job.user_id != session["user_id"]:
        return "Unauthorized"

    job.status = request.form.get("status")
    db.session.commit()

    flash("Status updated!")  # optional

    return redirect("/dashboard")


@jobs_bp.route("/drag-update/<int:id>", methods=["POST"])
def drag_update(id):

    if "user_id" not in session:
        return "Unauthorized"

    job = Job.query.get(id)

    if job.user_id != session["user_id"]:
        return "Unauthorized"

    new_status = request.form.get("status")

    job.status = new_status

    db.session.commit()

    return "Success"


# ---------------- EDIT JOB ----------------
@jobs_bp.route("/edit-job/<int:id>", methods=["GET", "POST"])
def edit_job(id):
    if "user_id" not in session:
        return redirect("/login")

    job = Job.query.get(id)

    if not job:
     return "Job not found"

    if job.user_id != session["user_id"]:
        return "Unauthorized"

    if request.method == "POST":
        job.company = request.form["company"]
        job.role = request.form["role"]
        job.status = request.form["status"]
        job.salary = request.form["salary"]
        job.work_type = request.form["work_type"]
        job.location = request.form["location"]
        job.notes = request.form["notes"]

        db.session.commit()

        flash("Job updated successfully!")  # 💎 NEW
        

        return redirect("/dashboard")
    return render_template("edit_job.html", job=job)

@jobs_bp.route("/upload-resume", methods=["GET", "POST"])
def upload_resume():

    if request.method == "POST":

        file = request.files["resume"]

        if file:

            filename = secure_filename(file.filename)

            filepath = os.path.join("uploads", filename)

            file.save(filepath)

            text = ""
        
            with open(filepath, "rb") as pdf_file:

             reader = PyPDF2.PdfReader(pdf_file)

             for page in reader.pages:

              text += page.extract_text()
              print(text)

            flash("Resume uploaded successfully!")

        required_skills = [
            "Python",
            "JavaScript",
            "React",
            "SQL",
            "API",
            "Flask",
            "HTML",
            "CSS"
        ]


        skills = []

        if "Python" in text:
            skills.append("Python")

        if "JavaScript" in text:
            skills.append("JavaScript")

        if "React" in text:
            skills.append("React")

        if "SQL" in text:
            skills.append("SQL")

        if "API" in text:
            skills.append("API")

        if "Flask" in text:
            skills.append("Flask")

        if "HTML" in text:
            skills.append("HTML")

        if "CSS" in text:
            skills.append("CSS")


        missing_skills = []

        for skill in required_skills:

            if skill not in skills:

                missing_skills.append(skill)


        score = min(
            100,
            40 + (len(skills) * 12)
        )


        if score < 60:

            suggestion = "Add more technical skills and projects."

        elif score < 80:

            suggestion = "Resume is strong but can improve with more experience."

        else:

            suggestion = "Excellent technical resume!"


        total_found = len(skills)

        total_missing = len(missing_skills)


        if score < 60:

            level = "Weak"
            color = "#ef4444"

        elif score < 80:

            level = "Good"
            color = "#facc15"

        else:

            level = "Strong"
            color = "#22c55e"


        analysis = {

            
            "ATS Score": f"{score}%",

            "Skills Found": skills,

            "Missing Skills": missing_skills,

            "Total Skills": total_found,

            "Missing Count": total_missing,

            "Resume Level": level,

            "Color": color,

            "Suggestion": suggestion
        }

        current_user.resume_score = f"{score}%"

        db.session.commit()


        return render_template(
            "upload_resume.html",
            analysis=analysis
        )


    return render_template(
        "upload_resume.html",
        analysis=None
    )

