from functools import wraps
from flask import request, redirect, url_for, session, render_template
# from datetime import datetime

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def error(message, code=400):
    return render_template("error.html", message=message, code=code), code

# class Message:
#     count = 1
#     time = datetime.utcnow()
#     def __init__(self, body, sender, channel):
#         self.body = body
#         self.sender = sender
#         self.channel = channel
#         self.time = datetime.utcnow()
#         self.timestamp = f"{self.time.hour}:{self.time.minute}, {self.time.year}-{self.time.month}-{self.time.day}"
#         self.id = Message.count
#         Message.count = Message.count + 1
