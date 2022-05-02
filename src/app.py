#  Gigawhat Website main application file.
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


# ------- Libraries, utils, and modules -------
from flask import abort, flash, make_response, redirect, render_template, request
from flask_security import hash_password
import jinja2
import werkzeug
from init import app, cache, db
from config import RENDER_CACHE_TIMEOUT
from modules.quiz import quiz_pages
from modules.blog import blog_pages
from modules.account import account_pages, user_datastore
from modules.database import database
from modules.temp_data import temp_data
from utils.helpers import translate


# ------- Blueprint registry -------
app.register_blueprint(quiz_pages, subdomain = "quiz")
app.register_blueprint(blog_pages, subdomain = "blog")
app.register_blueprint(account_pages)
app.register_blueprint(database)
app.register_blueprint(temp_data)


# ------- Global Jinja env variables -------
app.jinja_env.globals.update(translate = translate)


# ------- Error handlers -------
@app.errorhandler(werkzeug.exceptions.NotFound)
@cache.cached(timeout = RENDER_CACHE_TIMEOUT)
def error404(error):
    return render_template(request.cookies.get("lang") + "/errors/error_404.html"), 404

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@cache.cached(timeout = RENDER_CACHE_TIMEOUT)
def error500(error):
    return render_template(request.cookies.get("lang") + "/errors/error_500.html"), 500

@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
@cache.cached(timeout = RENDER_CACHE_TIMEOUT)
def error405(error):
    return render_template(request.cookies.get("lang") + "/errors/error_405.html"), 405

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@cache.cached(timeout = RENDER_CACHE_TIMEOUT)
def template_error(error):
    flash("gigawhat.net requires cookies to function properly.", "danger")
    return render_template("en_us/errors/error_500.html"), 500


# ------- Before request -------
@app.before_first_request
def create_user():
    if not user_datastore.find_user(email = "testme.com"):
        user_datastore.create_user(email = "testme.com", password = hash_password("password"), pp_url = "TESTESTESTEST")
    
    db.session.commit()

@app.before_request
def before_request():
    if not request.cookies.get("lang"): 
        response = make_response(redirect(request.url))
        response.set_cookie("lang", "en_us")
        
        return response


# ------- Cookie setters -------
@app.route("/set_lang_en", methods = ["POST"])
def set_lang_en():
    response = make_response(redirect(request.referrer))
    response.set_cookie("lang", "en_us")
        
    return response
    
@app.route("/set_lang_tr", methods = ["POST"])
def set_lang_tr():
    response = make_response(redirect(request.referrer))
    response.set_cookie("lang", "tr_tr")
        
    return response


# ------- Page routes -------
@app.route("/")
def index():
    posts = []
    
    posts.append({"title": "Placeholder post 1", "read_dur": "1963 mins", "thumb_url": "static/img/carousel/placeholder.png", "url": "#"})
    posts.append({"title": "Placeholder post 2", "read_dur": "1980 mins", "thumb_url": "static/img/carousel/placeholder.png", "url": "#"})
    posts.append({"title": "Placeholder post 3", "read_dur": "2001 mins", "thumb_url": "static/img/carousel/placeholder.png", "url": "#"})
    
    return render_template(request.cookies.get("lang") + "/index.html", page_views = 4444845, posts = posts)

@app.route("/mc-server")
def mc_server():
    return render_template(request.cookies.get("lang") + "/mc_server.html")

@app.route("/privacy-policy")
@cache.cached(timeout = RENDER_CACHE_TIMEOUT)
def privacy_policy():
    return render_template(request.cookies.get("lang") + "/privacy_policy.html")


# ------- Running the app -------
if __name__ == "__main__":
    db.create_all()
    app.run()