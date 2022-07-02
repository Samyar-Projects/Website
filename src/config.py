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
import logging
import os
import pkg_resources
from dotenv import load_dotenv


# ------- Load environment variables -------
load_dotenv("secrets/vars.env")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secrets/ga_creds.json"


# ------- Config classes -------
class ProductionConfig():
    # ------- Flask config -------
    SERVER_NAME = "gigawhat.net"
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY")
    DEBUG = False

    # ------- Flask-Caching config -------
    CACHE_DEFAULT_TIMEOUT = 0
    CACHE_TYPE = "FileSystemCache"
    CACHE_DIR = "__pycache__/FLASK_CACHE"

    # ------- Flask-SQLAlchemy config -------
    SQLALCHEMY_DATABASE_URI = "sqlite:///data/database/main.sqlite3"
    SQLALCHEMY_BINDS = {
        "accounts": "sqlite:///data/database/accounts.sqlite3",
        "quiz": "sqlite:///data/database/quiz.sqlite3"
    }
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ------- Flask-Security config -------
    SECURITY_PASSWORD_SALT = os.getenv("PASSWORD_ENCRYPT_SALT")
    SECURITY_PASSWORD_COMPLEXITY_CHECKER = "zxcvbn"
    SECURITY_REGISTERABLE = True
    SECURITY_PASSWORD_BREACHED_COUNT = 4
    SECURITY_REDIRECT_ALLOW_SUBDOMAINS = True
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = False
    SECURITY_I18N_DIRNAME = ["translations", pkg_resources.resource_filename("flask_security", "translations")]
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USERNAME_REQUIRED = True
    SECURITY_CONFIRMABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_PASSWORD_WITHIN = "2 days"
    SECURITY_TRACKABLE = True
    SECURITY_EMAIL_SENDER = "account@gigawhat.net"

    # ------- Mailjet config -------
    MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
    MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")

    # ------- Flask-WTF config -------
    WTF_CSRF_CHECK_DEFAULT = False

    # ------- Module configs -------
    QUIZ_QUESTION_COUNT = 15
    QUIZ_QUESTION_TIME = 60
    LOG_FILE_PATH = "../logs/"
    LOG_LEVEL = logging.INFO
    ANALYTICS_TAG_ID = "G-3J818WNF23"
    ANALYTICS_PROPERTY_ID = "315035421"
    MC_SERVER_TIMEOUT = 3.0
    TEMPORARY_FILE_DIR = "data/temporary"
    RENDER_CACHE_TIMEOUT = 3*60
    SUPPORTED_LANGS = ["en_US", "tr_TR"]


class TestingConfig(ProductionConfig):
    pass


class LocalConfig(ProductionConfig):
    SERVER_NAME = "gigawhat-local.gtw:5000"
    DEBUG = True
    RENDER_CACHE_TIMEOUT = 1


class AppConfig(ProductionConfig):
    # ------- Flask-Security config -------
    SECURITY_CHANGE_URL = "/change-pass"
    SECURITY_RESET_URL = "/reset-pass"
    SECURITY_SUBDOMAIN = "account"
    
    # ------- Flask-Security view overrides -------
    SECURITY_POST_LOGIN_VIEW = "index"
    SECURITY_POST_LOGOUT_VIEW = "index"
    SECURITY_CONFIRM_ERROR_VIEW = "login"
    SECURITY_POST_REGISTER_VIEW = "index"
    SECURITY_POST_CONFIRM_VIEW = "index"
    SECURITY_POST_RESET_VIEW = "login"
    SECURITY_POST_CHANGE_VIEW = "index"
    
    # ------- Flask-Security message overrides -------
    SECURITY_MSG_ALREADY_CONFIRMED = ("Your email has already been confirmed.", "info")
    SECURITY_MSG_API_ERROR = ("Input not appropriate for requested API", "danger")
    SECURITY_MSG_ANONYMOUS_USER_REQUIRED = ("You can only access this endpoint when not logged in.", "danger")
    SECURITY_MSG_CONFIRMATION_EXPIRED = ("You did not confirm your email within %(within)s. New instructions to confirm your email have been sent to %(email)s.", "danger")
    SECURITY_MSG_CONFIRMATION_REQUEST = ("Confirmation instructions have been sent to %(email)s.", "info")
    SECURITY_MSG_CONFIRMATION_REQUIRED = ("Email requires confirmation.", "danger")
    SECURITY_MSG_CONFIRM_REGISTRATION = ("Thank you. Confirmation instructions have been sent to %(email)s.", "success")
    SECURITY_MSG_DISABLED_ACCOUNT = ("Account is disabled.", "danger")
    SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = ("%(email)s is already associated with an account.", "danger")
    SECURITY_MSG_EMAIL_CONFIRMED = ("Thank you. Your email has been confirmed.", "success")
    SECURITY_MSG_EMAIL_NOT_PROVIDED = ("Email not provided", "danger")
    SECURITY_MSG_FAILED_TO_SEND_CODE = ("Failed to send code. Please try again later", "danger")
    SECURITY_MSG_FORGOT_PASSWORD = ("Forgot password?", "info")
    SECURITY_MSG_IDENTITY_ALREADY_ASSOCIATED = ("Identity attribute '%(attr)s' with value '%(value)s' is already associated with an account.", "danger")
    SECURITY_MSG_INVALID_CODE = ("Invalid code", "danger")
    SECURITY_MSG_INVALID_CONFIRMATION_TOKEN = ("Invalid confirmation token.", "danger")
    SECURITY_MSG_INVALID_EMAIL_ADDRESS = ("Invalid email address", "danger")
    SECURITY_MSG_INVALID_LOGIN_TOKEN = ("Invalid login token.", "danger")
    SECURITY_MSG_INVALID_PASSWORD = ("Invalid password", "danger")
    SECURITY_MSG_INVALID_PASSWORD_CODE = ("Password or code submitted is not valid", "danger")
    SECURITY_MSG_INVALID_REDIRECT = ("Redirections outside the domain are forbidden", "danger")
    SECURITY_MSG_INVALID_RESET_PASSWORD_TOKEN = ("Invalid reset password token.", "danger")
    SECURITY_MSG_LOGIN = ("Please log in to access this page.", "info")
    SECURITY_MSG_LOGIN_EMAIL_SENT = ("Instructions to login have been sent to %(email)s.", "success")
    SECURITY_MSG_LOGIN_EXPIRED = ("You did not login within %(within)s. New instructions to login have been sent to %(email)s.", "danger")
    SECURITY_MSG_PASSWORDLESS_LOGIN_SUCCESSFU = ("You have successfully logged in.", "success")
    SECURITY_MSG_PASSWORD_BREACHED = ("Password on breached list", "danger")
    SECURITY_MSG_PASSWORD_BREACHED_SITE_ERROR = ("Failed to contact breached passwords site", "danger")
    SECURITY_MSG_PASSWORD_CHANGE = ("You successfully changed your password.", "success")
    SECURITY_MSG_PASSWORD_INVALID_LENGTH = ("Password must be at least %(length)s characters", "danger")
    SECURITY_MSG_PASSWORD_IS_THE_SAME = ("Your new password must be different than your previous password.", "danger")
    SECURITY_MSG_PASSWORD_MISMATCH = ("Password does not match", "danger")
    SECURITY_MSG_PASSWORD_NOT_PROVIDED = ("Password not provided", "danger")
    SECURITY_MSG_PASSWORD_NOT_SET = ("No password is set for this user", "danger")
    SECURITY_MSG_PASSWORD_RESET = ("You successfully reset your password and you have been logged in automatically.", "success")
    SECURITY_MSG_PASSWORD_RESET_EXPIRED = ("You did not reset your password within %(within)s. New instructions have been sent to %(email)s.", "danger")
    SECURITY_MSG_PASSWORD_RESET_REQUEST = ("Instructions to reset your password have been sent to %(email)s.", "info")
    SECURITY_MSG_PASSWORD_TOO_SIMPLE = ("Password not complex enough", "danger")
    SECURITY_MSG_PHONE_INVALID = ("Phone number not valid e.g. missing country code", "danger")
    SECURITY_MSG_REAUTHENTICATION_REQUIRED = ("You must re-authenticate to access this endpoint", "danger")
    SECURITY_MSG_REAUTHENTICATION_SUCCESSFUL = ("Reauthentication successful", "info")
    SECURITY_MSG_REFRESH = ("Please reauthenticate to access this page.", "info")
    SECURITY_MSG_RETYPE_PASSWORD_MISMATCH = ("Passwords do not match", "danger")
    SECURITY_MSG_TWO_FACTOR_INVALID_TOKEN = ("Invalid Token", "danger")
    SECURITY_MSG_TWO_FACTOR_LOGIN_SUCCESSFUL = ("Your token has been confirmed", "success")
    SECURITY_MSG_TWO_FACTOR_CHANGE_METHOD_SUCCESSFUL = ("You successfully changed your two-factor method.", "success")
    SECURITY_MSG_TWO_FACTOR_PERMISSION_DENIED = ("You currently do not have permissions to access this page", "danger")
    SECURITY_MSG_TWO_FACTOR_METHOD_NOT_AVAILABLE = ("Marked method is not valid", "danger")
    SECURITY_MSG_TWO_FACTOR_DISABLED = ("You successfully disabled two factor authorization.", "success")
    SECURITY_MSG_UNAUTHORIZED = ("You do not have permission to view this resource.", "danger")
    SECURITY_MSG_UNAUTHENTICATED = ("You are not authenticated. Please supply the correct credentials.", "danger")
    SECURITY_MSG_US_METHOD_NOT_AVAILABLE = ("Requested method is not valid", "danger")
    SECURITY_MSG_US_SETUP_EXPIRED = ("Setup must be completed within %(within)s. Please start over.", "danger")
    SECURITY_MSG_US_SETUP_SUCCESSFUL = ("Unified sign in setup successful", "info")
    SECURITY_MSG_US_SPECIFY_IDENTITY = ("You must specify a valid identity to sign in", "danger")
    SECURITY_MSG_USE_CODE = ("Use this code to sign in: %(code)s.", "info")
    SECURITY_MSG_USER_DOES_NOT_EXIST = ("Specified user does not exist", "danger")
    SECURITY_MSG_USERNAME_INVALID_LENGTH = ("Username must be at least %(min)d characters and less than %(max)d characters", "danger")
    SECURITY_MSG_USERNAME_ILLEGAL_CHARACTERS = ("Username contains illegal characters", "danger")
    SECURITY_MSG_USERNAME_DISALLOWED_CHARACTERS = ("Username can contain only letters and numbers", "danger")
    SECURITY_MSG_USERNAME_NOT_PROVIDED = ("Username not provided", "danger")
    SECURITY_MSG_USERNAME_ALREADY_ASSOCIATED = ("%(username)s is already associated with an account.", "danger")