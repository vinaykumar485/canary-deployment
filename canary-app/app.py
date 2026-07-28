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
    <body style="font-family:Arial; text-align:center; margin-top:100px;">
        <h1>Hello from {VERSION}</h1>

        <h2>Argo Rollouts Canary Deployment Demo</h2>

        <hr width="50%">

        <h3>Version : {VERSION}</h3>

        <h3>Pod Name : {hostname}</h3>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
