#  Gigawhat Website blog module.
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

"""
Redirect module for the Gigawhat website.

This module is for social and or other redirects.
"""


# ------- Libraries and utils -------
from flask import Blueprint, redirect, url_for
from flask_babel import get_locale
from flask_security import url_for_security


# ------- Blueprint init -------
redirects = Blueprint("redirects", __name__)


# ------- Page redirects -------
@redirects.route("/quiz")
def quiz_redirect():
    return redirect(url_for("quiz_pages.index"))


@redirects.route("/blog")
def blog_redirect():
    return redirect(url_for("blog_pages.index"))


@redirects.route("/forum")
def forum_redirect():
    return redirect(url_for("forum_pages.index"))


@redirects.route("/login")
def login_redirect():
    return redirect(url_for_security("login"))


@redirects.route("/register")
def register_redirect():
    return redirect(url_for_security("register"))


@redirects.route("/signup")
def signup_redirect():
    return redirect(url_for_security("register"))


# ------- Social redirects -------
@redirects.route("/twitter")
def twitter_redirect():
    if str(get_locale()) == "en_US":
        return redirect("https://twitter.com/Gigawhat_net")
    
    return redirect("https://twitter.com/Gigawhat_net_tr")


@redirects.route("/instagram")
def instagram_redirect():
    if str(get_locale()) == "en_US":
        return redirect("https://www.instagram.com/gigawhat_net/")

    return redirect("https://www.instagram.com/gigawhat_net_tr/")


@redirects.route("/discord")
def discord_redirect():
    if str(get_locale()) == "en_US":
        return redirect("https://discord.gg/rMq7GujUZJ")
    
    return redirect("https://discord.gg/bSHkhaGeuN")


@redirects.route("/youtube")
def youtube_redirect():
    if str(get_locale()) == "en_US":
        return redirect("https://www.youtube.com/channel/UCgjkgNz1MbhzIzhOOHfrxiw")
    
    return redirect("https://www.youtube.com/channel/UCfjmMzekHS1YI2pv2tpvS2g")


@redirects.route("/patreon")
def patreon_redirect():
    return redirect("https://www.patreon.com/gigawhat")


@redirects.route("/github")
def github_redirect():
    return redirect("https://github.com/Gigawhat-net")


@redirects.route("/open-source")
def opensource_redirect():
    return redirect("https://github.com/Gigawhat-net")


@redirects.route("/email")
def email_redirect():
    if str(get_locale()) == "en_US":
        return redirect("mailto:contact@gigawhat.net")
    
    return redirect("mailto:contact.tr@gigawhat.net")