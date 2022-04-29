#  Gigawhat Website blog module.
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


# ------- Libraries and utils -------
from flask import Blueprint, abort, make_response, redirect, render_template, request


# ------- Blueprint init -------
blog_pages = Blueprint("blog_pages", __name__, template_folder = "../templates", static_folder = "../static")


# ------- Cookie setters -------
@blog_pages.route("/set_lang_en", methods = ["POST", "GET"])
def set_lang_en():
    if request.method == "POST":
        response = make_response(redirect(request.referrer))
        response.set_cookie("lang", "en_us")
        
        return response
    
    else:
        abort(404)
    
@blog_pages.route("/set_lang_tr", methods = ["POST", "GET"])
def set_lang_tr():
    if request.method == "POST":
        response = make_response(redirect(request.referrer))
        response.set_cookie("lang", "tr_tr")
        
        return response
    
    else:
        abort(404)
        
        
# ------- Page routes -------
@blog_pages.route('/')
def index():
    return render_template(request.cookies.get("lang") + "/blog_index.html", pp_url = "https://torange.biz/photofxnew/76/IMAGE/lion-profile-picture-76801.jpg", username = "TestUser")