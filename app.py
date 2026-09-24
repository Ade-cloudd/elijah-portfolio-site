from flask import Flask, render_template, request, redirect, url_for, flash
import boto3
from botocore.exceptions import ClientError
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret-change-in-production")

AWS_REGION = os.environ.get("AWS_REGION", "eu-west-2")
DYNAMODB_TABLE = os.environ.get("DYNAMODB_TABLE", "portfolio-contact-messages")

dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/experience")
def experience():
    return render_template("experience.html")

@app.route("/certifications")
def certifications():
    return render_template("certifications.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("contact"))

        try:
            table = dynamodb.Table(DYNAMODB_TABLE)
            table.put_item(Item={
                "message_id": str(uuid.uuid4()),
                "name": name,
                "email": email,
                "message": message,
                "submitted_at": datetime.utcnow().isoformat()
            })
            flash("Thanks for reaching out, I'll get back to you soon.", "success")
        except ClientError as e:
            flash("Something went wrong, please try again later.", "error")
            print(f"DynamoDB error: {e}")

        return redirect(url_for("contact"))

    return render_template("contact.html")

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)