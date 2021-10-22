from flask import Flask, jsonify, request, session, redirect
import uuid
from flask.templating import render_template
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import redirect


class User:
    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):


        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }

        # encrypt password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])
        from app import db
        #check for existing email
        if db.users.find_one({ "email": user['email'] }):
            return jsonify({"error":"Email address already in use"}), 400

       
        if db.users.insert_one(user):
            return self.start_session(user)

        return jsonify({ "error": "Signup failed" }), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):


        from app import db
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid Credentials" }), 401


    def forget_password(self):
        user = { 'email': request.form.get('email') }
        from app import mail, db
        if db.users.find_one({ "email": user['email'] }):
            mail.send_message('New message from',
                    sender='dpradnya757@gmail.com',
                    recipients=[user['email']],
                    body="Here is the new password")
            return jsonify({"error": "Mail sent" }), 200
        
        return jsonify({"error": "Pls reenter email" }), 401
        