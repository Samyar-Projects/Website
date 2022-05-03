#  Gigawhat Website database module.
#  Copyright 2022 Gigawhat Programming Team
#  Written by Samyar Sadat Akhavi, 2022.
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
from flask import Blueprint, flash, render_template, request
from flask_security import RoleMixin, UserMixin
from init import db


# ------- Blueprint init -------
database = Blueprint("database", __name__)


# ------- Temporary page route -------
@database.route("/quiz-db-add", methods = ["GET", "POST"])
def quiz_db_add():
    if request.method == "POST":
        try:
            q = request.form.get("q")
            aa = request.form.get("aa")
            ab = request.form.get("ab")
            ac = request.form.get("ac")
            ad = request.form.get("ad")
            ca = request.form.get("ca")
            cat = request.form.get("cat")
            diff = request.form.get("diff")
            lvl = request.form.get("lvl")
            lang = request.form.get("lang")
            
            data = QuizQuestions(cat, lang, lvl, diff, q, ca, aa, ab, ac, ad, True)
            db.session.add(data)
            db.session.commit()

        except:
            flash("ERROR", "danger")
            return render_template("en_us/quiz/db_add.html")
        
        else:
            flash("SUCCESS", "success")
            return render_template("en_us/quiz/db_add.html")
    
    else:
        return render_template("en_us/quiz/db_add.html")


# ------- Database models -------

# ---- User database ----
class RolesUsers(db.Model):
    __tablename__ = "RolesUsers"
    
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("Users.id"))
    role_id = db.Column("role_id", db.Integer, db.ForeignKey("Role.id"))

class Role(db.Model, RoleMixin):
    __tablename__ = "Role"
    
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True)
    description = db.Column(db.String(255))

class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(255), unique = True)
    username = db.Column(db.String(255), unique = True)
    pp_url = db.Column(db.String(255))
    password = db.Column(db.String(255), nullable = False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique = True, nullable = False)
    confirmed_at = db.Column(db.DateTime)
    
    roles = db.relationship("Role", secondary = "RolesUsers", backref = db.backref("users", lazy = "dynamic"))
        
# ---- Quiz Question Database ----
class QuizQuestions(db.Model):
    __tablename__ = "QuizQuestions"
    
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20))
    lang = db.Column(db.String(5))
    level = db.Column(db.Integer)
    difficulty = db.Column(db.String(15))
    question = db.Column(db.String(16384), unique = True)
    correct_answ = db.Column(db.String(1))
    answ_a = db.Column(db.String(2048))
    answ_b = db.Column(db.String(2048))
    answ_c = db.Column(db.String(2048))
    answ_d = db.Column(db.String(2048))
    status = db.Column(db.Boolean)
    
    def __init__(self, category, lang, level, difficulty, question, correct_answ, answ_a, answ_b, answ_c, answ_d, status):
        self.category = category
        self.lang = lang
        self.level = level
        self.difficulty = difficulty
        self.question = question
        self.correct_answ = correct_answ
        self.answ_a = answ_a
        self.answ_b = answ_b
        self.answ_c = answ_c
        self.answ_d = answ_d
        self.status = status
        
# ---- Quiz Result Database ----
class QuizResults(db.Model):
    __tablename__ = "QuizResults"
    
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.String(10))
    time = db.Column(db.String(8))
    multiplayer = db.Column(db.Boolean)
    player_1_with_account = db.Column(db.Boolean)
    player_2_with_account = db.Column(db.Boolean)
    player_1 = db.Column(db.String(50))
    player_2 = db.Column(db.String(50))
    quiz_id = db.Column(db.String(32), unique = True)
    player_1_wrong = db.Column(db.Integer)
    player_1_right = db.Column(db.Integer)
    player_2_wrong = db.Column(db.Integer)
    player_2_right = db.Column(db.Integer)
    
    def __init__(self, date, time, player_1_with_account, player_2_with_account, player_1, player_2, quiz_id, player_1_wrong, player_1_right, player_2_wrong, player_2_right):
        self.date = date
        self.time = time
        self.player_1_with_account = player_1_with_account
        self.player_2_with_account = player_2_with_account
        self.player_1 = player_1
        self.player_2 = player_2
        self.quiz_id = quiz_id
        self.player_1_wrong = player_1_wrong
        self.player_1_right = player_1_right
        self.player_2_wrong = player_2_wrong
        self.player_2_right = player_2_right
        
        if(player_2):
            self.multiplayer = True
            
        else:
            self.multiplayer = False