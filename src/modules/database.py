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

"""
Database module for the Gigawhat website.

This module contains all of the database models.
"""


# ------- Libraries and utils -------
import json
from flask import Blueprint, flash, render_template, request
from flask_security import RoleMixin, SQLAlchemySessionUserDatastore, UserMixin
from init import db, log
from utils.models import MCMod


# ------- Blueprint init -------
database = Blueprint("database", __name__)


# ------- Temporary page route -------
@database.route("/quiz-db-add", methods=["GET", "POST"])
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
            subcat = request.form.get("subcat")
            diff = request.form.get("diff")
            lvl = request.form.get("lvl")
            lang = request.form.get("lang")

            data = QuizQuestions(cat, subcat, lang, lvl, diff, q, ca, aa, ab, ac, ad, True)
            db.session.add(data)
            db.session.commit()
            
            flash("SUCCESS", "success")
            return render_template("quiz/db_add.html")

        except Exception as e:
            log.exception("AddQuizQuestionException")
            flash(e, "danger")
            return render_template("quiz/db_add.html")

    else:
        return render_template("quiz/db_add.html")
    
    
@database.route("/mc-server-db-add", methods=["GET", "POST"])
def mc_server_db_add():
    if request.method == "POST":
        try:
            ed = request.form.get("ed")
            d_ip = request.form.get("dip")
            ip = request.form.get("ip")
            port = request.form.get("port")
            desc = request.form.get("desc")
            modload = request.form.get("ml")
            mods = request.form.get("mods")
            mzip = request.form.get("mzip")
                
            if modload == "None" or mods == "None" or mzip == "None" or modload == None or mods == None or mzip == None or modload == "" or mods == "" or mzip == "":
                modload = None
                f_mods = None
                mzip = None
                                
            else:
                mods = mods.split(";")
                f_mods = []
                
                for mod in mods:
                    data = json.loads(mod)
                    f_mods.append(data)
                
            if port == "None" or port == None or port == "":
                data = MinecraftServer(ed, d_ip, ip, None, json.loads(desc), modload, mzip, f_mods, True)
                
            else:
                data = MinecraftServer(ed, d_ip, ip, int(port), json.loads(desc), modload, mzip, f_mods, True)
                
            db.session.add(data)
            db.session.commit() 
            
            flash("SUCCESS", "success")
            return render_template("mc_server_db_add.html")
            
        except Exception as e:
            log.exception("AddQuizQuestionException")
            flash(e.with_traceback, "danger")
            return render_template("mc_server_db_add.html")
        
    else:
        return render_template("mc_server_db_add.html")


# ------- Database models -------

# -=-=-= Accounts database =-=-=-
# ---- User roles table ----
class RolesUsers(db.Model):
    __bind_key__ = "accounts"
    __tablename__ = "RolesUsers"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("Users.id"))
    role_id = db.Column("role_id", db.Integer, db.ForeignKey("Role.id"))


# ---- Roles table ----
class Role(db.Model, RoleMixin):
    __bind_key__ = "accounts"
    __tablename__ = "Role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# ---- User table ----
class Users(db.Model, UserMixin):
    __bind_key__ = "accounts"
    __tablename__ = "Users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), unique=True)
    pp_url = db.Column(db.String(255), default="img/logos/default_pp.png")
    password = db.Column(db.String(255), nullable=False)
    last_login_at = db.Column(db.DateTime)
    current_login_at = db.Column(db.DateTime)
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    confirmed_at = db.Column(db.DateTime)

    roles = db.relationship("Role", secondary="RolesUsers", backref=db.backref("users", lazy="dynamic"))


# -=-=-= Quiz database =-=-=-
# ---- Quiz question table ----
class QuizQuestions(db.Model):
    __bind_key__ = "quiz"
    __tablename__ = "QuizQuestions"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(30))
    subcategory = db.Column(db.String(50))
    lang = db.Column(db.String(5))
    level = db.Column(db.Integer)
    difficulty = db.Column(db.String(15))
    question = db.Column(db.String(16384), unique=True)
    correct_answ = db.Column(db.String(1))
    answ_a = db.Column(db.String(2048))
    answ_b = db.Column(db.String(2048))
    answ_c = db.Column(db.String(2048))
    answ_d = db.Column(db.String(2048))
    status = db.Column(db.Boolean)

    def __init__(self, category: str, subcategory: str, lang: str, level: int, difficulty: str, question: str, correct_answ: str, answ_a: str, answ_b: str, answ_c: str, answ_d: str, status: bool):
        self.category = category
        self.subcategory = subcategory
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


# ---- Quiz result table ----
class QuizResults(db.Model):
    __bind_key__ = "quiz"
    __tablename__ = "QuizResults"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10))
    time = db.Column(db.String(8))
    multiplayer = db.Column(db.Boolean)
    quiz_id = db.Column(db.String(32), unique=True)
    player_info = db.Column(db.JSON)

    def __init__(self, date: str, time: str, multiplayer: bool, quiz_id: str, player_info):
        self.date = date
        self.time = time
        self.multiplayer = multiplayer
        self.quiz_id = quiz_id
        self.player_info = player_info
        
        
# -=-=-= Minecraft server database =-=-=-
# ---- Server table ----
class MinecraftServer(db.Model):
    __tablename__ = "MinecraftServer"

    id = db.Column(db.Integer, primary_key=True)
    edition = db.Column(db.String(8))
    display_ip_add = db.Column(db.String(64))
    ip_add = db.Column(db.String(16))
    port = db.Column(db.Integer, nullable=True)
    desc = db.Column(db.JSON)
    modded = db.Column(db.Boolean)
    modloader = db.Column(db.String(16), nullable=True)
    mods = db.Column(db.JSON, nullable=True)
    mods_zip = db.Column(db.String(2048), nullable=True)
    status = db.Column(db.Boolean)

    def __init__(self, edition: str, display_ip_add: str, ip_add: str, port: int, desc: dict, modloader: str, mods: list, mods_zip: str, status: bool):
        self.edition = edition
        self.display_ip_add = display_ip_add
        self.ip_add = ip_add
        self.port = port
        self.desc = desc
        self.modloader = modloader
        self.mods = mods
        self.mods_zip = mods_zip
        self.status = status
        
        if modloader and mods:
            self.modded = True
            
        else:
            self.modded = False


# ------- Flask-Security user datastore -------
user_datastore = SQLAlchemySessionUserDatastore(db.session, Users, Role)
