import os
from flask import Flask, flash, redirect, render_template, request


# Configuring the application
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")