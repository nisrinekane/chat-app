from flask import Flask, render_template, redirect, request, session, flash, jsonify
from flask_socketio import SocketIO, send
from flask_bcrypt import Bcrypt     

app = Flask(__name__)
app.secret_key = "9619ec889b6c53e806bced52a3d50276"
socketio = SocketIO(app, cors_allowed_origins='*')

bcrypt = Bcrypt(app)

# chat route 
@app.route('/chat')
def chat():
    if 'user_id' in session:
        user_id = session['first_name'].upper()
    else:
        user_id = 'Customer Agent'
    return render_template('chat.html', user_id = user_id)

socketio = SocketIO(app, cors_allowed_origins='*')

@socketio.on('message')
def handleMessage(msg):
	print(msg)
	send(msg, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='localhost')