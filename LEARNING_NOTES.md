# CareerPilot Learning Notes

## Simple Rule

- Say "start learning" to continue coding lessons.
- Say "upgrade CareerPilot" to improve the project code.
- We will learn only using this CareerPilot project.
- Each lesson will be small.
- After each lesson, there will be a short quiz.

## What You Know Now

You understand these things:

- `python app.py` starts the website.
- Python is backend.
- HTML is frontend.
- Database saves data.
- `/login`, `/dashboard`, `/add-job` are routes/pages.
- `GET` means open/show page.
- `POST` means send form data.
- `session["user_id"]` remembers the logged-in user.
- `db.session.add(...)` gets data ready to save.
- `db.session.commit()` saves data in database.
- `user_id` in Job tells which user owns that job.

## Easy Meaning Of Important Words

### Backend

Backend is Python code.

Backend does things like:

- login
- register
- save job
- delete job
- talk to database
- read PDF

### Frontend

Frontend is what user sees.

Frontend uses:

- HTML
- CSS
- JavaScript

Examples:

- buttons
- forms
- text boxes
- dashboard page
- login page

### Database

Database saves information.

In CareerPilot, database saves:

- username
- password
- jobs
- company name
- role
- status
- resume score

## render_template vs redirect

### render_template

```python
return render_template("login.html")
```

Simple meaning:

```text
Show this HTML page.
```

### redirect

```python
return redirect("/dashboard")
```

Simple meaning:

```text
Send user to another page.
```

## GET vs POST

### GET

GET means user is opening a page.

Example:

```text
User opens /login
```

### POST

POST means user is sending form data.

Example:

```text
User types username/password and clicks Login.
```

Easy memory:

```text
GET = show page
POST = send form
```

## Forms

HTML input:

```html
<input name="username">
```

Python reads it:

```python
username = request.form.get("username")
```

Important:

```text
The names must match exactly.
```

Correct:

```html
<input name="salary">
```

```python
request.form.get("salary")
```

Wrong:

```html
<input name="job_salary">
```

```python
request.form.get("salary")
```

Because `job_salary` and `salary` are not the same name.

## Add Job Flow

When user adds a job:

```text
1. User fills Add Job form.
2. User clicks button.
3. HTML sends data to Python.
4. Python receives company, role, status, etc.
5. Python creates a new Job.
6. Python saves Job in database.
7. User goes back to dashboard.
```

Code:

```python
new_job = Job(
    company=company,
    role=role,
    status=status,
    user_id=session["user_id"]
)
```

Simple meaning:

```text
Create one new job for the logged-in user.
```

Then:

```python
db.session.add(new_job)
db.session.commit()
```

Simple meaning:

```text
Prepare to save.
Actually save.
```

## Database Models

`models.py` tells database what tables and columns exist.

Example:

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
```

Simple table:

```text
User
id | username
1  | tanvi
2  | hello
```

### id

`id` is automatic number from database.

User does not type it.

Example:

```text
First user gets id 1
Second user gets id 2
Third user gets id 3
```

### primary_key=True

Simple meaning:

```text
This is the main ID of the row.
```

### nullable=False

Simple meaning:

```text
This cannot be empty.
```

Example:

```python
username = db.Column(db.String(100), nullable=False)
```

Means username is required.

### unique=True

Simple meaning:

```text
Duplicate is not allowed.
```

Example:

```python
username = db.Column(db.String(100), unique=True)
```

Means two users cannot have same username.

### ForeignKey

Example:

```python
user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
```

Simple meaning:

```text
This job belongs to one user.
```

## Session

When user logs in, your app saves:

```python
session["user_id"] = user.id
```

Simple meaning:

```text
Remember this logged-in user.
```

Example:

```text
Tanvi logs in.
Tanvi's user id is 1.
App remembers session["user_id"] = 1.
```

Then dashboard checks:

```python
if "user_id" not in session:
    return redirect("/login")
```

Simple meaning:

```text
If user is not logged in, send them to login page.
```

## Lessons Completed

```text
Lesson 1: How website runs
Lesson 2: GET vs POST
Lesson 3: Add Job flow
Lesson 4: Database models
```

## Mistakes To Practice

### Mistake 1

Wrong:

```python
request.form.get["salary"]
```

Correct:

```python
request.form.get("salary")
```

### Mistake 2

Wrong idea:

```text
id is typed by user.
```

Correct idea:

```text
id is created automatically by database.
```

## Last Quiz Result

You answered well.

You understood:

- `nullable=False`
- `unique=True`
- `user_id`
- `models.py`

Need more practice:

- `id`
- database relationship between `User` and `Job`

## Next Lesson

Next lesson:

```text
Lesson 5: Database IDs and Relationships
```

We will learn:

- what `id` is
- why database needs IDs
- how `User` connects to `Job`
- how dashboard shows only your jobs
- why one user cannot see another user's jobs

## Super Short Summary

```text
Python = brain/backend
HTML = page/frontend
Database = storage
Route = URL/page door
GET = open page
POST = send form
session = remember logged-in user
id = automatic database number
user_id = tells who owns the data
commit = save to database
```
