from flask import Flask, request, redirect
import json
import os

app = Flask(__name__)
FILE = "reels.json"

def load_reels():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def save_reels(reels):
    with open(FILE, "w") as f:
        json.dump(reels, f)

@app.route("/", methods=["GET", "POST"])
def home():
    reels = load_reels()

    filter_type = request.args.get("filter", "All")
    search = request.args.get("search", "").lower()

    if request.method == "POST":
        link = request.form.get("link")
        category = request.form.get("category")
        username = request.form.get("username")
        note = request.form.get("note")

        if link:
            reels.append({
                "link": link,
                "category": category,
                "username": username,
                "note": note,
                "favorite": False
            })
            save_reels(reels)

        return redirect("/")

    html = """
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="manifest" href="/static/manifest.json">
<meta name="theme-color" content="#f8f7f5">
<title>Reel Saver</title>

<style>
body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont;
    background: #f8f7f5;
}

/* App container */
.phone {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
.header {
    padding: 14px;
    text-align: center;
    font-weight: 500;
    font-size: 15px;
    border-bottom: 1px solid #eee;
    background: #f8f7f5;
}

/* Content */
.content {
    flex: 1;
    overflow-y: auto;
    padding: 14px;
}

/* Inputs */
input, select {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: 1px solid #eee;
    margin-bottom: 8px;
    background: white;
}

/* Button */
button {
    width: 100%;
    padding: 12px;
    border-radius: 12px;
    border: none;
    background: #111;
    color: white;
    margin-bottom: 12px;
}

/* Grid */
.grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
}

/* Card */
.card {
    background: white;
    padding: 10px;
    border-radius: 16px;
    border: 1px solid #eee;
}

/* Preview */
.preview {
    height: 100px;
    border-radius: 12px;
    background: #f0f0f0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: #999;
    margin-bottom: 6px;
}

/* Text */
.category {
    font-weight: 500;
    font-size: 13px;
}

.small {
    font-size: 11px;
    color: #888;
}

/* Links */
a {
    text-decoration: none;
    font-size: 12px;
    color: #444;
}

/* Bottom nav */
.nav {
    display: flex;
    justify-content: space-around;
    padding: 10px;
    border-top: 1px solid #eee;
    background: white;
}
.nav a {
    color: #666;
}
</style>
</head>

<body>

<div class="phone">

<div class="header">Reel Saver 🎀</div>

<div class="content">

<form method="POST">
    <input name="link" placeholder="Paste reel link" required>
    <input name="username" placeholder="@username">
    <input name="note" placeholder="Idea / notes">

    <select name="category">
        <option value="Beauty">Beauty</option>
        <option value="Fashion">Fashion</option>
        <option value="Ideas">Ideas</option>
        <option value="Aesthetic">Aesthetic</option>
    </select>

    <button>Save</button>
</form>

<form method="GET">
    <input name="search" placeholder="Search...">
</form>

<div class="grid">
"""

    for i, r in enumerate(reels):
        if isinstance(r, dict):

            # FILTER
            if filter_type == "Fav" and not r.get("favorite"):
                continue
            if filter_type != "All" and filter_type != "Fav" and r["category"] != filter_type:
                continue

            # SEARCH
            if search and search not in (r.get("note","") + r.get("username","")).lower():
                continue

            html += f'''
<div class="card">

    <div class="preview">🎬</div>

    <div class="category">{r["category"]}</div>
    <div class="small">{r.get("username","")}</div>
    <div class="small">{r.get("note","")}</div>

    <a href="{r["link"]}" target="_blank">Open</a><br>

    <a href="/fav/{i}">{"❤️" if r.get("favorite") else "🤍"}</a>
    <a href="/delete/{i}" style="color:red;">Delete</a>

</div>
'''

    html += """
</div>
</div>

<div class="nav">
    <a href="/?filter=All">Home</a>
    <a href="/?filter=Beauty">Beauty</a>
    <a href="/?filter=Fashion">Fashion</a>
    <a href="/?filter=Fav">❤️</a>
</div>

</div>

</body>
</html>
"""

    return html


@app.route("/delete/<int:index>")
def delete(index):
    reels = load_reels()
    if 0 <= index < len(reels):
        reels.pop(index)
        save_reels(reels)
    return redirect("/")


@app.route("/fav/<int:index>")
def fav(index):
    reels = load_reels()
    if 0 <= index < len(reels):
        reels[index]["favorite"] = not reels[index].get("favorite", False)
        save_reels(reels)
    return redirect("/")


@app.route("/manifest.json")
def manifest():
    return app.send_static_file("manifest.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)