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
from flask import Blueprint
from init import db


# ------- Blueprint init -------
database = Blueprint("database", __name__)


# ------- Database models -------

# ---- User database ----
class Users(db.Model):
    __tablename__ = "Users"
    
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50), unique = True)
    password = db.Column(db.String(121))
    username = db.Column(db.String(50), unique = True)
    pp_url = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    
    def __init__(self, email, password, username, pp_url, admin):
        self.email = email
        self.password = password
        self.username = username
        self.pp_url = pp_url
        self.admin = admin
        
# ---- Quiz Question Database ----
class QuizQuestions(db.Model):
    __tablename__ = "QuizQuestions"
    
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(20))
    lang = db.Column(db.String(5))
    level = db.Column(db.Integer)
    difficulty = db.Column(db.String(15))
    question = db.Column(db.String(16384))
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