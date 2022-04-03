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


# ------- Libraries and utils -------
from flask import abort, make_response, redirect, render_template, request, session
from init import app, cache
from modules.quiz import quiz_pages


# ------- Blueprint registry -------
app.register_blueprint(quiz_pages, subdomain = "quiz")


# ------- Error handlers -------
@app.errorhandler(404)
@cache.cached(timeout = 2)
def error404(error):
    return "<h1>Error 404 - Not Found</h1>", 404


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
    return render_template(request.cookies.get("lang") + "/index.html", logged_in = True, pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")


# ------- Running the app -------
if __name__ == "__main__":
    app.run()