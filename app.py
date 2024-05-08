# app.py

from flask import Flask, render_template, redirect, url_for, request
import firebase_admin
from firebase_admin import credentials, firestore, auth
import extData

app = Flask(__name__)

# Initialize Firebase Admin SDK with your credentials
cred = credentials.Certificate('./firebase.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore DB
db = firestore.client()

@app.route('/')
def homePage():
    return render_template('index.html')

@app.route('/contact')
def contactPage():
    return render_template('contact.html')
# Route for the find page
@app.route('/find')
def findPage():
    # Check if user is authenticated
    #try:
    #id_token = request.cookies.get("token")
    #decoded_token = auth.verify_id_token(id_token)
    #user_id = decoded_token['uid']

    # Retrieve data from Firestore
    docs = db.collection('cards').list_documents()
    data = []
    for doc in docs:
        doc_data = doc.get().to_dict()
        data.append(doc_data)

    return render_template('find.html', data=data)

    #except Exception as e:
        # Redirect to authentication page if user is not authenticated
        #return redirect(url_for('authPage'))
# Route for the authentication page
@app.route('/auth')
def authPage():
    return render_template('auth.html')

# Function to push data to Firestore
def push_data_to_firestore(data):
    for idx, item in enumerate(data):
        doc_ref = db.collection('cards').document(f'card-{idx + 1}')
        doc_ref.set(item)

    print("Data has been successfully pushed to Firestore.")


@app.route('/events')
def eventPage():
    return render_template('events.html')
# Sample data
rawData = extData.rawData

# Push sample data to Firestore
push_data_to_firestore(rawData)

if __name__ == '__main__':
    app.run(debug=True)
