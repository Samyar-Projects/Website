#  Samyar Projects Website blog module.
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
Blog module for the Samyar Projects Website.

Notes
-----
This module is not complete.
"""


# ------- Libraries and utils -------
from flask import Blueprint, render_template


# ------- Blueprint init -------
blog_pages = Blueprint("blog_pages", __name__, template_folder="../templates", static_folder="../static")


# ------- Page routes -------
@blog_pages.route("/")
def index():
    return render_template("blog_index.html")
