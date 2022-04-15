# Copyright 2022 Gigawhat Programming Team
# User profile, login, and signup module.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#     
# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# ------- Libraries and utils -------
from random import randint
import re
import json
from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from init import cache, db
from modules.database import users
from utils.helpers import check_email_validity, check_password_validity, translate
import flask_login
from randimage import get_random_image
import matplotlib
import threading


# ------- Blueprint init -------
account_pages = Blueprint("account_pages", __name__, template_folder = "../templates", static_folder = "../static")


# ------- Page routes -------
@account_pages.route("/login")
def login():
    return render_template(request.cookies.get("lang") + "/login.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

@account_pages.route("/signup", methods = ["GET", "POST"])
def signup():
    lang = request.cookies.get("lang")
    
    if request.method == "GET":        
        return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

    elif request.method == "POST":

        email = request.form.get("email")     
        password = request.form.get("password")
        rep_password = request.form.get("rep_password")
            
        if not email and not password and not rep_password:
            flash(translate("invalid_input", lang), "danger")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")
            
        if not check_email_validity(email):
            flash(translate("invalid_email", lang), "danger")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")
        
        if password != rep_password:
            flash(translate("pass_dont_match", lang), "warning")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")
            
        if users.query.filter_by(email = email).first():
            flash(translate("duplicate_email", lang), "warning")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

        if not check_password_validity(password):
            flash(translate("invalid_pass", lang), "danger")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

        username = email.split("@")
        username = username[0]
                    
        while users.query.filter_by(username = username).first():
            username = username + "_" + str(randint(0, 999))
                    
        img_res = (12, 12)
        img = get_random_image(img_res)
        matplotlib.image.imsave("static/img/profile_pictures/" + username + ".png", img)
                    
        user = users(email, generate_password_hash(password, method = "sha384"), username, "../../static/img/profile_pictures/" + username + ".png", False)
                    
        db.session.add(user)
        db.session.commit()
                    
        flash(translate("signup_success", lang), "success")
        return redirect(url_for("account_pages.login"))        