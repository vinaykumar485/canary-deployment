from flask import Flask
import os

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v2")

@app.route("/")
def home():

    hostname = os.getenv("HOSTNAME", "Unknown")

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Argo Rollouts Demo</title>
    </head>

    <body style="font-family:Arial;text-align:center;margin-top:80px;">

        <h1>Argo Rollouts Canary Deployment</h1>

        <hr width="60%">

        <h2>Application Version : {VERSION}</h2>

        <h3>Pod Name : {hostname}</h3>

        <h2 style="color:green;">Welcome to Version 2</h2>

        <p>This is the Canary Release.</p>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
