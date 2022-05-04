#  Gigawhat Website flask and flask plugin config file.
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


# ------- Libraries -------
import os
import pkg_resources


# ------- Load env variables -------
from dotenv import load_dotenv
load_dotenv("vars.env")


# ------- Flask config -------
# SERVER_NAME = "gigawhat-local.gtw:5000"
SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
# DEBUG = True


# ------- Flask-Caching config -------
CACHE_DEFAULT_TIMEOUT = 0
CACHE_TYPE = "FileSystemCache"
CACHE_DIR = "CACHE"


# ------- Flask-SQLAlchemy config -------
SQLALCHEMY_DATABASE_URI = "sqlite:///data/database/db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = True


# ------- Flask-Security config -------
SECURITY_PASSWORD_SALT = os.getenv("PASSWORD_ENCRYPT_SALT")
SECURITY_PASSWORD_COMPLEXITY_CHECKER = "zxcvbn"
SECURITY_REGISTERABLE = True
SECURITY_PASSWORD_BREACHED_COUNT = 4
SECURITY_REDIRECT_ALLOW_SUBDOMAINS = True
SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True
SECURITY_I18N_DIRNAME = [pkg_resources.resource_filename("flask_security", "translations"), "translations"]
SECURITY_USERNAME_ENABLE = True
SECURITY_USERNAME_REQUIRED = True
SECURITY_CONFIRMABLE = True
SECURITY_CHANGEABLE = True
SECURITY_CHANGE_URL = "/change-pass"
SECURITY_RECOVERABLE = True
SECURITY_RESET_URL = "/reset-pass"
SECURITY_RESET_PASSWORD_WITHIN = "2 days"
SECURITY_TRACKABLE = True
SECURITY_EMAIL_SENDER = "contact@gigawhat.net"


# ------- Flask-Mail config -------
MAIL_SERVER = "smtp.googlemail.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_USERNAME = os.getenv("FLASK_MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("FLASK_MAIL_PASSWORD")
MAIL_DEFAULT_SENDER = "contact@gigawhat.net"


# ------- Flask-WTF config -------
WTF_CSRF_CHECK_DEFAULT = False


# ------- Module configs -------
QUIZ_QUESTION_COUNT = 3
QUIZ_QUESTION_TIME = 60
TEMPORARY_FILE_DIR = "data/temporary"
RENDER_CACHE_TIMEOUT = 1