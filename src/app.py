# Copyright 2022 Gigawhat Programming Team
# Main application file.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, 
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#     
# The above copyright notice and this permission notice shall be included in all copies or substantial 
# portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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
@app.errorhandler(werkzeug.exceptions.NotFound)
@cache.cached(timeout = 2)
def error404(error):
    return "<h1>Error 404 - Not Found</h1>", 404

@app.errorhandler(werkzeug.exceptions.InternalServerError)
@cache.cached(timeout = 2)
def error500(error):
    return "<h1>Error 500 - Internal Server Error</h1>", 500

@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
@cache.cached(timeout = 2)
def error405(error):
    return "<h1>Error 405 - Method Not Allowed</h1>", 405

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@cache.cached(timeout = 2)
def template_error(error):
    return "<h1>Error 500 - Internal Server Error (TemplateError)</h1>", 500


# ------- Before request -------
@app.before_request
def before_request():
    if not request.cookies.get("lang"): 
        response = make_response(redirect(request.url))
        response.set_cookie("lang", "en_us")
        
        return response
    
    else:
        pass


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
    
    posts.append({"title" : "Test Title 1", "read_dur" : "10 mins", "thumb_url" : "static/img/carousel/placeholder.png", "url" : "#"})
    posts.append({"title" : "Test Title 2", "read_dur" : "3 mins", "thumb_url" : "static/img/carousel/placeholder.png", "url" : "#"})
    posts.append({"title" : "Doctor Who?", "read_dur" : "1963 mins", "thumb_url" : "static/img/carousel/placeholder.png", "url" : "#"})
    
    return render_template(request.cookies.get("lang") + "/index.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser", page_views = 123, posts = posts)

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