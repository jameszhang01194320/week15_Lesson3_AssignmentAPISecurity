Lesson 3: Assignment | API Security

Task 1: Implement JWT Token Generation
•	Add the pyjwt library to the requirements.txt file to enable JWT token generation and validation.
===============================
>>pip install pyjwt
>>pip freeze > requirements.txt
===============================
•	Create a utils folder and generate the util.py file to create tokens and validate tokens as required.
•	Define a secret key to be used for creating the JWT tokens.
===============================
util.py:
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify

SECRET_KEY = 'my_secert_token'
===============================
•	Implement a function named encode_token(user_id) in util.py to generate JWT tokens with an expiration time, issued time (iat), and user ID as the payload.
===============================
def encode_token(user_id): #original
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(hours=1), #setting an expiration date
        'iat': datetime.now(timezone.utc), #Issued at
        'sub': user_id #Sub stands for 'subject' aka who is this token for
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token
===============================

Task 2: Authentication Logic
•	create a login route for your Customer blueprint that takes in email and password.
•	Utilize the encode_token function from the util.py module you created to generate the JWT token with the user ID as the payload.
•	Return the JWT token along with a success message upon successful authentication.
===============================
customerController.py

from utils.util import token_required
def login():
    try: 
        credentials = customer_login.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400 #invalid credential payload
    
    token = customerService.login(credentials)

    if token:
        response = {
            "status": "success",
            "message": "successfully logged in",
            "token": token
        }
        return jsonify(response), 200
    else:
        return jsonify({"status": "error", "message": "invalid username or password"}), 404


customerService.py

def login(credentials):
    query = select(Customer).where(Customer.email == credentials['email'])
    customer = db.session.execute(query).scalar_one_or_none()

    if customer and customer.password == credentials['password']: #if there is a customer, check their password
        auth_token = encode_role_token(customer.id, customer.admin)
        return auth_token
    
    return None


===============================

Task 3: Create a token_required wrapper
•	Back in the util.py file, create a wrapper that will validate your tokens past in as Authorization headers.
•	Remember the value of your auth header 'Authorization: 'Bearer <token>'
•	Ensure to let the user know if the token has expired, or is invalid


Task 4: Add access control
•	Utilize your @token_required wrapper on resources, you think the user should be logged in to use. (apply it to at least one controller)
===============================
We use it in customerController def find_all():

@token_required
def find_all():

   Users should log in to use find all, to protect the privacy of customers

===============================

