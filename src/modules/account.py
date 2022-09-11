#  Samyar Projects Website user account module.
#  Copyright 2022 Samyar Projects
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
User account module for the Samyar Projects Website.

The user account module contains the profile, settings, and
user-specific status pages.

Notes
-----
The rest of the user account system (login, logout, signup, ext.)
is handled by Flask-Security.

This module is not complete.
"""


# ------- Libraries and utils -------
from flask import Blueprint, redirect, url_for
from flask_security import Security
from init import app
from modules.database import user_datastore
from utils.email import SecurityMailUtil


# ------- Flask-Security init -------
security = Security(app, user_datastore, mail_util_cls=SecurityMailUtil)


# ------- Blueprint init -------
account_pages = Blueprint("account_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Page routes -------
@account_pages.route("/")
def index():
    return redirect(url_for("index"))
