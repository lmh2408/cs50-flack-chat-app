import os

from flask import Flask, render_template, session, redirect, request, url_for, jsonify, escape
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

from helpers import login_required, error

# SECRET_KEY=b'\xa15\x00\x0e\xa4M\xd0\x14\xfd4'
# FLASK_APP=application.py
# FLASK_ENV=development


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["TEMPLATES_AUTO_RELOAD"] = True
socketio = SocketIO(app)


# channel list
channels_list = list()
message_data = {}

@app.route("/register", methods=["POST"])
def register():
    """ Log user in """
    if session.get("username"):
        return redirect(url_for("board"))
    username = request.form.get("username")
    session["username"] = username
    return redirect(url_for("board"))


@app.route("/")
def index():
    if session.get("username"):
        return redirect(url_for("board"))
    else:
        return render_template("index.html")


@app.route("/logout")
def logout():
    """ Log user out """
    session.clear()
    return redirect(url_for("index"))


@app.route("/board")
@login_required
def board():
    """ Page to display and create channel """
    if session.get("current_channel"):
        if session.get("current_channel") in channels_list:
            return redirect(url_for("channel", channel_name = session.get("current_channel")))
    return render_template("board.html", name=session["username"])


@app.route("/channel/<channel_name>")
@login_required
def channel(channel_name):
    """ Channel page """
    # check if channels_name is valid
    if channel_name not in channels_list:
        return error("No such channel exists")
    session["current_channel"] = channel_name
    return render_template("channel.html", channel_name=channel_name)


@app.route("/exit")
def exit():
    session["current_channel"] = ""
    return redirect(url_for("board"))


@socketio.on("add_channel")
def add_channel(data):
    """ Add new channel to list """
    # get input
    new_channel = data["new_channel"]

    # check if channel already exists or empty, then create appropriate response
    if not new_channel or new_channel in channels_list:
        response = {"add_success": False}
    else:
        channels_list.append(new_channel)
        response = {"add_success": True, "added_channel": new_channel}
        message_data[new_channel]= []

    emit("add_channel_response", response)
    emit("channels_list", channels_list, broadcast=True)


@socketio.on("display_channel")
def list_channel():
    """ Send list of channels """
    emit("channels_list", channels_list, broadcast=True)


@socketio.on("joinchannel")
def joinchannel(data):
    """ Signal to join channel """
    join_room(data["channel_name"])

    emit("show_message", message_data[session.get("current_channel")], room=data["channel_name"])


@socketio.on("get_message")
def get_message(data):
    """ Receive message """
    # check message
    if not data["message"]:
        pass

    # get current datetime
    time = datetime.utcnow()
    timestamp = time.strftime("%H:%M, %Y-%m-%d")

    # prepare data format
    message = {"message": escape(data["message"]), "timestamp": timestamp, "sender": session.get("username")}

    # add message to message_data
    message_data[session.get("current_channel")].append(message)

    # delete first message if message count exceed 100
    if len(message_data[session.get("current_channel")]) > 100:
        message_data[session.get("current_channel")].pop(0)

    emit("show_message", message_data[session.get("current_channel")], room=session.get("current_channel"))


if __name__ == '__main__':
    socketio.run(app)
