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
import jinja2
import werkzeug
from flask import abort, redirect, render_template, request, session, url_for
from flask_security import hash_password, url_for_security
from flask_babel import get_locale
from init import app, cache, db, babel, log
from config import RENDER_CACHE_TIMEOUT, SUPPORTED_LANGS
from modules.quiz import quiz_pages
from modules.blog import blog_pages
from modules.account import account_pages
from modules.database import database, user_datastore
from modules.temp_data import temp_data


# ------- Jinja env global objects -------
app.jinja_env.globals["get_locale"] = get_locale
app.jinja_env.globals["SUPPORTED_LANGS"] = SUPPORTED_LANGS


# ------- Blueprint registry -------
app.register_blueprint(quiz_pages, subdomain="quiz")
app.register_blueprint(blog_pages, subdomain="blog")
app.register_blueprint(account_pages, subdomain="account")
app.register_blueprint(database)
app.register_blueprint(temp_data)


# ------- Locale selector ------- 
@app.route("/set-lang/<lang>", methods=["POST"])
def set_lang(lang):
    log.debug(f"[{request.remote_addr}] Changed language to [{lang}]")
    
    if lang in SUPPORTED_LANGS:
        session["lang"] = lang
        return redirect(request.referrer)
    
    abort(500)

@babel.localeselector
def get_locale():
    lang = session.get("lang")
    
    if lang:
        return lang

    session["lang"] = request.accept_languages.best_match(SUPPORTED_LANGS)
    return session.get("lang")


# ------- Error handlers -------
@app.errorhandler(werkzeug.exceptions.NotFound)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error404(error):
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [404 Error]")
    return render_template("errors/error_404.html"), 404

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error500(error):
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [500 Error]")
    return render_template("errors/error_500.html"), 500

@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error405(error):
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [405 Error]")
    return render_template("errors/error_405.html"), 405

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def template_error(error):
    log.warning(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [500 Template Error]")
    return render_template("errors/error_500.html"), 500


# ------- Before request -------
@app.before_first_request
def create_user():
    if not user_datastore.find_user(email="test@me.com"):
        user_datastore.create_user(email="test@me.com", password=hash_password("password"))
    
    db.session.commit()

@app.before_request
def remove_www():
    if "://www." in request.url.lower():
        log.info(f"[{request.remote_addr}] Sent a request with [www.]")
        
        request_url=request.url.lower()
        return redirect(request_url.replace("www.", ""))
    
@app.before_request
def request_logging():
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}]")


# ------- Page routes -------
@app.route("/")
def index():
    posts = []
    
    posts.append({"title": "Placeholder post 1", "read_dur": "1963 mins", "thumb_url": "img/carousel/placeholder.png", "url": "#"})
    posts.append({"title": "Placeholder post 2", "read_dur": "1980 mins", "thumb_url": "img/carousel/placeholder.png", "url": "#"})
    posts.append({"title": "Placeholder post 3", "read_dur": "2001 mins", "thumb_url": "img/carousel/placeholder.png", "url": "#"})
    
    return render_template("index.html", page_views=4444845, posts=posts)

@app.route("/mc-server")
def mc_server():
    return render_template("mc_server.html")

@app.route("/privacy-policy")
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def privacy_policy():
    return render_template("privacy_policy.html")


# ------- Page redirects -------
@app.route("/quiz")
def quiz_redirect():
    return redirect(url_for("quiz_pages.index"))

@app.route("/blog")
def blog_redirect():
    return redirect(url_for("blog_pages.index"))

@app.route("/login")
def login_redirect():
    return redirect(url_for_security("login"))

@app.route("/register")
def register_redirect():
    return redirect(url_for_security("register"))

@app.route("/signup")
def signup_redirect():
    return redirect(url_for_security("register"))


# ------- Running the app -------
if __name__ == "__main__":
    db.create_all()
    app.run()