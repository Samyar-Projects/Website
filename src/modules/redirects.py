#  Samyar Projects Website blog module.
#  Copyright 2021-2023 Samyar Sadat Akhavi
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
Redirect module for the Samyar Projects Website.

This module is for social and or other redirects.
"""


# ------- Libraries and utils -------
from flask import Blueprint, redirect, send_from_directory, url_for
from flask_babel import get_locale
from flask_security import url_for_security
from config import AppConfig
from init import debug_log, log


# ------- Blueprint init -------
redirects = Blueprint("redirects", __name__, static_folder="../static")


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
@redirects.route("/signup")
def register_redirect():
    return redirect(url_for_security("register"))


# ------- Social redirects -------
@redirects.route("/twitter")
def twitter_redirect():
    url = AppConfig.TWITTER_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [TWITTER_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [TWITTER_URL] redirect with language [{str(get_locale())}]")
    abort(404)


"""
@redirects.route("/instagram")
def instagram_redirect():
    url = AppConfig.INSTAGRAM_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [INSTAGRAM_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [INSTAGRAM_URL] redirect with language [{str(get_locale())}]")
    abort(404)
"""


@redirects.route("/dc")
@redirects.route("/discord")
def discord_redirect():
    url = AppConfig.DISCORD_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [DISCORD_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [DISCORD_URL] redirect with language [{str(get_locale())}]")
    abort(404)


@redirects.route("/yt")
@redirects.route("/youtube")
def youtube_redirect():
    url = AppConfig.YOUTUBE_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [YOUTUBE_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [YOUTUBE_URL] redirect with language [{str(get_locale())}]")
    abort(404)


"""
@redirects.route("/patreon")
def patreon_redirect():
    url = AppConfig.PATREON_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [PATREON_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [PATREON_URL] redirect with language [{str(get_locale())}]")
    abort(404)
"""


@redirects.route("/open-source")
@redirects.route("/github")
def github_redirect():
    url = AppConfig.GITHUB_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [GITHUB_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [GITHUB_URL] redirect with language [{str(get_locale())}]")
    abort(404)


@redirects.route("/mail")
@redirects.route("/email")
def email_redirect():
    url = AppConfig.EMAIL_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [EMAIL_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [EMAIL_URL] redirect with language [{str(get_locale())}]")
    abort(404)


@redirects.route("/spforum-ban-appeal")
def spforum_ban_appeal_redirect():
    url = AppConfig.FORUM_BAN_APPEAL_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [FORUM_BAN_APPEAL_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [FORUM_BAN_APPEAL_URL] redirect with language [{str(get_locale())}]")
    abort(404)


@redirects.route("/discord-ban-appeal")
def discord_ban_appeal_redirect():
    url = AppConfig.DISCORD_BAN_APPEAL_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [DISCORD_BAN_APPEAL_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [DISCORD_BAN_APPEAL_URL] redirect with language [{str(get_locale())}]")
    abort(404)


@redirects.route("/server-suggestions")
def server_suggestions_redirect():
    url = AppConfig.SERVER_SUGGESTIONS_URL[str(get_locale())]
    
    if url:
        return redirect(url)

    log.error(f"[{request.remote_addr}] Failed to load URL for [SERVER_SUGGESTIONS_URL] redirect with language [{str(get_locale())}]")
    debug_log.debug(f"[{request.remote_addr}] Failed to load URL for [SERVER_SUGGESTIONS_URL] redirect with language [{str(get_locale())}]")
    abort(404)