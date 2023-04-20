from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_mail import Mail, Message
import re
import preprocessing
import numpy as np
from werkzeug.security import generate_password_hash
from flask import Flask, session, request, jsonify
# from flask_login import LoginManager, login_user, logout_user, UserMixin
# from flask_mysqldb import MySQL
from flask import Flask, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, session
from flask import Flask, session
from flask_session import Session
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from keras.models import load_model
from flask_login import login_required
import redis
app = Flask(__name__)
# app.config['MODELS'] = {
#     'model1': tf.keras.models.load_model("D://University/IIT/level 6/FYP/BackendFyp/model/priority model.h5"),
#     'model2': tf.keras.models.load_model("D://University/IIT/level 6/FYP/BackendFyp/model/modelSeverity3SmotENN.h5")
# }
model_1 = load_model("./model/priority model.h5")
model_2 = load_model("./model/modelSeverity3SmotENN.h5")

# Set up MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fyp'
mysql = MySQL(app)
# Set up Flask-Login
# app.secret_key = 'my-secret-key'
login_manager = LoginManager()
login_manager.init_app(app)

# configure Flask to use Redis as the session store
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
# app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'secret_key'
# Configure session to use a secure cookie
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True

# Initialize the session extension
Session(app)

cors = CORS(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'sbugclassifier@gmail.com'
app.config['MAIL_PASSWORD'] = 'bugClassifier123.'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)
priority=""
severity=""
detailList=[]


def priorityPredictions(input_data):
    # priority = model_1.predict(input_data, axis=-1)
    # Predict the class using the pre-loaded model
    y_pred = model_1.predict(input_data)

    # Convert the predicted probabilities to class labels
    y_pred_priority_class= np.argmax(y_pred, axis=-1)

    # Return the predicted class
    return y_pred_priority_class
    # print(priority)
    # return priority

def severityPredictions(input_data):

    y_pred = model_2.predict(input_data)

    # Convert the predicted probabilities to class labels
    y_pred_severity_class = np.argmax(y_pred, axis=-1)

    # Return the predicted class
    return y_pred_severity_class

# Login route
@app.route("/login", methods=[ "GET","POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()

    if user and check_password_hash(user[3], password):
        session['user'] = {'id': user[0],'email': user[1], 'username': user[2]}
        print(session["user"])
        return jsonify(session['user'])
    else:
        return jsonify({'error': 'Invalid username or password'})

@app.route("/logout", methods=["GET"])
def logout():
    session.pop("user", None)
    return jsonify({"message": "Logged out successfully"})

@app.route("/user", methods=["GET"])

def get_user():
    # user = session.get('user')
    if user in session:
        print((session["user"]))
        return jsonify(session["user"])
    # if user:
    #     print(user)
    #     return jsonify(user)
    else:
        return jsonify({"error": "User not logged in"})

@app.route('/signup', methods=[ "GET","POST"])
def signup():

    email = request.json["email"]
    username = request.json["username"]
    password = request.json["password"]
    print(email)
    print(username)
    print(password)
    if not email or not username or not password:
        return jsonify({'error': 'All fields are required'}), 400

    hashed_password = generate_password_hash(password)

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO users (email, username, password) VALUES (%s, %s, %s)',
                (email, username, hashed_password))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/deleteProfile', methods=["GET","POST",'DELETE'])
def delete_profile():
    # if 'user' not in session:
    #     return jsonify({'error': 'User not authenticated'})
    username = request.json["username"]
    print(username)
    if 'username' == "":
        return jsonify({'error': 'Username not provided'})

    # user_id = session['user']['id']
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM users WHERE username = %s', (username,))
    mysql.connection.commit()
    cur.close()
    session.clear()
    # session.pop('user', None)
    return jsonify({'message': 'Profile deleted successfully'})



@app.route("/send", methods=[ "GET","POST"])
def send():
    if request.method == "POST":
        title = str(request.json["title"])
        description = str(request.json["description"])
        # print("title")
        cleanDescription= preprocessing.preprocess_text(description)
        print(cleanDescription)
        emotionScore=preprocessing.sentiment_scores(cleanDescription)
        # print(emotionScore)
        scores=emotionScore
        sentiment_scores = [[scores['pos'],scores['neg'], scores['neu'] ]]
        print(sentiment_scores)
        try:

            # loadedModel=preprocessing.loadmodel()
            # y_pred_class = np.argmax(loadedModel.predict(sentiment_scores), axis=-1)
            # y_pred = model.predict(X_test)
            y_pred_class=priorityPredictions(sentiment_scores)
            print(y_pred_class)
            if(y_pred_class== 0):
                priority="High"
            if (y_pred_class == 1):
                priority = "Medium"
            if (y_pred_class == 2):
                priority = "Low"

            # loadedModelSeverity = preprocessing.loadmodelSeverity()
            # severity_pred_class = np.argmax(loadedModelSeverity.predict(sentiment_scores), axis=-1)
            severity_pred_class=severityPredictions(sentiment_scores)
            print(severity_pred_class)
            if (severity_pred_class == 0):
                severity = "critical"
            if (severity_pred_class == 1):
                severity = "blocker"
            if (severity_pred_class == 2):
                severity = "major"
            if (severity_pred_class == 3):
                severity = "minor"
            if (severity_pred_class == 4):
                severity = "trivial"
            if (severity_pred_class == 5):
                severity = "normal"
            if (severity_pred_class == 6):
                severity = "enhancement"

            return jsonify({"title":title,"description":description,"severity":severity,"priority":priority})
        except Exception as e:
            return(jsonify({'message': 'Error .Please try again'}))
    else:
        return(jsonify({'message': 'Error .Please try again'}))

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route("/mail", methods=['POST'])
def sendMail():

    # detailList.clear()
    # details = request.get_json(['details'])
    # detailList.append(details)
    # emailAddress = detailList[0]["mail"]
    # name = detailList[0]["name"]
    name = str(request.json["name"])
    emailAddress = str(request.json["email"])
    message = str(request.json["message"])

    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(regex, emailAddress)):
        msg = Message('Working with Us', sender='sbugclassifier@gmail.com', recipients=[emailAddress])
        msg.body = "Hello "+name+"!! Thankyou for contacting us.We will look into your message and contact you within 3-4 business days"
        mail.send(msg)
        status = 1
    else:
        status = 0
    return jsonify(status)




if __name__ == '__main__':
    app.run()
