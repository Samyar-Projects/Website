#  Gigawhat Website user account login and signup module.
#  Copyright 2022 Gigawhat Programming Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


# ------- Libraries and utils -------
from random import randint
from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash
from init import db
from modules.database import Users
from utils.helpers import check_email_validity, check_password_validity, translate
from randimage import get_random_image
import matplotlib


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
            
        if Users.query.filter_by(email = email).first():
            flash(translate("duplicate_email", lang), "warning")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

        if not check_password_validity(password):
            flash(translate("invalid_pass", lang), "danger")
            return render_template(lang + "/signup.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

        username = email.split("@")
        username = username[0]
                    
        while Users.query.filter_by(username = username).first():
            username = username + "_" + str(randint(0, 999))
                    
        img_res = (12, 12)
        img = get_random_image(img_res)
        matplotlib.image.imsave("static/img/profile_pictures/" + username + ".png", img)
                    
        user = Users(email, generate_password_hash(password, method = "sha384"), username, "../../static/img/profile_pictures/" + username + ".png", False)
                    
        db.session.add(user)
        db.session.commit()
                    
        flash(translate("signup_success", lang), "success")
        return redirect(url_for("account_pages.login"))        