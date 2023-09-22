import datetime
import json
from flask import Flask, make_response, render_template, request, redirect, session, jsonify, flash, url_for
import base64
import mysql.connector
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_ROOT_PASSWORD'] = 'pass'
app.config['MYSQL_DATABASE'] = 'chatAppDB'
app.config['MYSQL_HOST'] = '192.168.128.1'

mysql = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_ROOT_PASSWORD'],
    database=app.config['MYSQL_DATABASE']
)

# Create a cursor to execute SQL queries
cursor = mysql.cursor()

#region helper functions
def encode_password(password):
    encoded_bytes = base64.b64encode(password.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_password(encoded_password):
    decoded_bytes = base64.b64decode(encoded_password.encode('utf-8'))
    return decoded_bytes.decode('utf-8')
#endregion

#region register
@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        # encoded_pass = encode_password(userpass)
        encoded_pass = userpass
        
        # Check if the user already exists    
        cursor.execute('SELECT * FROM Users WHERE Username = %s', (username,))
        user = cursor.fetchone()
       
        if user is not None:
            # return redirect("/login")
            return redirect('/lobby')

            # return "The user already exists"
        
        # Insert into the DB
        cursor.execute('INSERT INTO Users (Username, Password) VALUES (%s, %s)', (username, userpass))
        mysql.commit()  # Call commit() on the database connection object
        
        # After inserting, query the database to fetch the user's data
        cursor.execute('SELECT * FROM Users WHERE Username = %s', (username,))
        user = cursor.fetchone()

        # Check if the user was found
        if user:
            # User found, print the user's data
            print("User ID:", user[0])
            print("Username:", user[1])
            # You can print or display more user data as needed
        else:
            # User not found, handle the case where the user was not inserted
            print("User not found in the database")
        # cursor.close()
        return redirect("/login")
        
    return render_template("register.html")

#endregion

#region login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']

        cursor.execute('SELECT * FROM Users WHERE Username = %s AND Password = %s', (username, userpass))
        user = cursor.fetchone()
        if user is not None:
            print(f"User {username} logged in successfully")
            session['username'] = username
            return redirect('/lobby')
        else:
            print(f"Failed login attempt for user {username}")
    return render_template('login.html')
#endregion

#region lobby
@app.route('/lobby', methods=['GET', 'POST'])
def lobby():
    if 'username' in session:
        if request.method == 'POST':
            room_name = request.form['new_room']
            cursor.execute('SELECT * FROM Rooms WHERE RoomName = %s', (room_name,))
            room = cursor.fetchone()
            
            # Check if room name already exists
            if room is not None:
                return "The given room name already exists"
            else:
                cursor.execute('INSERT INTO Rooms (RoomName) VALUES (%s)', (room_name,))
                mysql.commit()  # Call commit() on the database connection object
                print("CREATED NEW ROOM NAMED: " + room_name)    
            
        rooms = []
        cursor.execute('SELECT * FROM Rooms')
        for row in cursor:
            rooms.append(row[1])

        return render_template('lobby.html', rooms=rooms)
    else:
        return redirect('/login')
#endregion

#region logout
@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect("/login")

#endregion

#region chat ( This function handles the chat page)
@app.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    if 'username' in session:
        return render_template('chat.html', room=room)
    else:
        return redirect('/login')
#endregion

#region updateChat 
@app.route('/api/chat/<room>', methods=['GET','POST'])
def updateChat(room):
    username = session['username']
    room_name=room
    
    if request.method == 'POST':
        if not room_name:
            return "Invalid room_name"


        # Get the new message from the request
        new_message = request.form['msg']
                
        # Get the user ID from the session
        cursor.execute('SELECT Userid FROM Users WHERE Username = %s', (username,))
        user_id = cursor.fetchone()
        # user_id = session['user_id']

        # Format the date and time as a string
        current_datetime = datetime.datetime.now()
        # formatted_datetime = current_datetime.strftime("[%Y-%m-%d %H:%M:%S]")
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
        cursor.execute('INSERT INTO Messages (UserID,RoomName,Content,Timestamp) VALUES (%s, %s, %s, %s)', (user_id[0],room_name,new_message,formatted_datetime))
        mysql.commit() 
     
    
    cursor.execute('SELECT * FROM Messages WHERE RoomName = %s', (room_name,))
    messages = cursor.fetchall()
    return jsonify([session['username'], messages])


#endregion


#region health check
@app.route("/health")
def health():
    return "OK", 200

#endregion

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

