#  Gigawhat Website main application file.
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


# ------- Libraries, utils, and modules -------
from flask import abort, make_response, redirect, render_template, request, session
import jinja2
import werkzeug
from init import app, cache, db
from modules.quiz import quiz_pages
from modules.blog import blog_pages
from modules.account import account_pages
from modules.database import database


# ------- Blueprint registry -------
app.register_blueprint(quiz_pages, subdomain = "quiz")
app.register_blueprint(blog_pages, subdomain = "blog")
app.register_blueprint(account_pages)
app.register_blueprint(database)


# ------- Error handlers -------
cache_time = 10*60

@app.errorhandler(werkzeug.exceptions.NotFound)
@cache.cached(timeout = cache_time)
def error404(error):
    return "<h1>Error 404 - Not Found</h1>", 404

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@cache.cached(timeout = cache_time)
def error500(error):
    return "<h1>Error 500 - Internal Server Error</h1>", 500

@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
@cache.cached(timeout = cache_time)
def error405(error):
    return "<h1>Error 405 - Method Not Allowed</h1>", 405

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@cache.cached(timeout = cache_time)
def template_error(error):
    return "<h1>Error 500 - Internal Server Error (TemplateError)</h1>", 500


# ------- Before request -------
@app.before_request
def before_request():
    if not request.cookies.get("lang"): 
        response = make_response(redirect(request.url))
        response.set_cookie("lang", "en_us")
        
        return response


# ------- Cookie setters -------
@app.route("/set_lang_en", methods = ["POST", "GET"])
def set_lang_en():
    if request.method == "POST":
        response = make_response(redirect(request.referrer))
        response.set_cookie("lang", "en_us")
        
        return response
    
    else:
        abort(404)
    
@app.route("/set_lang_tr", methods = ["POST", "GET"])
def set_lang_tr():
    if request.method == "POST":
        response = make_response(redirect(request.referrer))
        response.set_cookie("lang", "tr_tr")
        
        return response
    
    else:
        abort(404)


# ------- Page routes -------
@app.route("/")
def index():
    posts = []
    
    posts.append({"title": "Placeholder post 1", "read_dur": "1963 mins", "thumb_url": "static/img/carousel/placeholder.png", "url": "#"})
    posts.append({"title": "Placeholder post 2", "read_dur": "1980 mins", "thumb_url": "static/img/carousel/placeholder.png", "url": "#"})
    posts.append({"title": "Placeholder post 3", "read_dur": "2001 mins", "thumb_url": "static/img/carousel/placeholder.png", "url": "#"})
    
    return render_template(request.cookies.get("lang") + "/index.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser", page_views = 4444845, posts = posts)

@app.route("/mc-server")
def mc_server():
    return render_template(request.cookies.get("lang") + "/mc_server.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")

@app.route("/privacy-policy")
def privacy_policy():
    return render_template(request.cookies.get("lang") + "/privacy_policy.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")


# ------- Running the app -------
if __name__ == "__main__":
    db.create_all()
    app.run()