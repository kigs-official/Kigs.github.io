from flask import Flask, render_template, 
request, redirect, url_for, session from 
flask_socketio import SocketIO, send from 
flask_login import LoginManager, UserMixin, 
login_user, login_required, logout_user, 
current_user import redis app = Flask(__name__) 
app.config['SECRET_KEY'] = 'your_secret_key' 
socketio = SocketIO(app, 
cors_allowed_origins="*")
# Redis for temporary message storage
redis_client = 
redis.StrictRedis(host='localhost', port=6379, 
decode_responses=True)
# User authentication setup
login_manager = LoginManager() 
login_manager.init_app(app)
# Dummy user database
users = {"user1": "pass1", "user2": "pass2"} 
class User(UserMixin):
    def __init__(self, username): self.id = 
        username
@login_manager.user_loader def 
load_user(user_id):
    return User(user_id) if user_id in users 
    else None
@app.route('/', methods=['GET', 'POST']) def 
login():
    if request.method == 'POST': username = 
        request.form['username'] password = 
        request.form['password'] if username in 
        users and users[username] == password:
            user = User(username) 
            login_user(user) return 
            redirect(url_for('chat'))
    return render_template('login.html') 
@app.route('/chat') @login_required def chat():
    return render_template('chat.html', 
    username=current_user.id)
@socketio.on('message') def 
handle_message(msg):
    redis_client.rpush("chat", 
    f"{current_user.id}: {msg}") 
    send(f"{current_user.id}: {msg}", 
    broadcast=True)
@app.route('/logout') @login_required def 
logout():
    logout_user() return 
    redirect(url_for('login'))
if __name__ == '__main__':
    socketio.run(app, debug=True)
