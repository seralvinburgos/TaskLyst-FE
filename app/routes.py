import json

import requests
from flask import Flask, render_template, request, redirect

BACKEND_URL = "http://127.0.0.1:5000/tasks"

app = Flask(__name__)


@app.get("/")
def view_home_page():
    return render_template("index.html")


@app.get("/list")
def view_task_list():
    response = requests.get(BACKEND_URL)
    response = response.json()
    return render_template(
            "list.html", 
            tasks=response["tasks"]
    )


@app.get("/task/<int:task_id>")
def view_task_by_id(task_id):
    url = "%s/%s" % (BACKEND_URL, task_id)
    response = requests.get(url).json()
    return render_template(
            "detail.html", 
            task=response["task"], 
    )


@app.get("/task/new")
def task_form():
    return render_template("new.html")


@app.post("/task/new")
def create_task():
    raw_data = request.form
    task_json = {
        "title": raw_data.get("title"),
        "subtitle": raw_data.get("subtitle"),
        "body": raw_data.get("body")
    }
    response = requests.post(BACKEND_URL, json=task_json)
    if response.status_code == 201:
        return render_template("create_success.html")
    else:
        return render_template("create_failure.html")


@app.get("/task/update/<int:task_id>")
def update_task_by_id(task_id):
    url = "%s/%s" % (BACKEND_URL, task_id)
    response = requests.get(url).json()
    return render_template(
            "update.html", 
            task=response["task"], 
    )


@app.post("/task/update/<int:task_id>")
def update_task(task_id):
    raw_data = request.form
    task_json = { 
        "title": raw_data.get("title"),
        "subtitle": raw_data.get("subtitle"),
        "body": raw_data.get("body")
    }
    url = "%s/%s" % (BACKEND_URL, task_id)
    response = requests.put(url, json=task_json)
    if response.status_code == 204:
        return render_template("update_success.html")
    else:
        return render_template("update_failure.html")


@app.get("/task/delete/<int:task_id>")
def delete_task_by_id(task_id):
    url = "%s/%s" % (BACKEND_URL, task_id)
    response = requests.delete(url)
    if response.status_code == 204:
        return render_template("delete_success.html")
    else:
        return render_template("delete_failure.html") 