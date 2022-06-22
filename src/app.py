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
from flask import abort, redirect, render_template, request, session
from config import AppConfig
from flask_babel import get_locale
from init import app, cache, db, babel, log, debug_log, bedrock_servers, java_servers
from modules.quiz import quiz_pages
from modules.blog import blog_pages
from modules.forum import forum_pages
from modules.account import account_pages
from modules.database import database
from modules.redirects import redirects
from modules.api import api
from utils.models import HomeNews, MCServer, MCMod
from utils.google_analytics import Analytics
from utils.mc_server import JavaServer, BedrockServer


# ------- Global variables -------
SUPPORTED_LANGS = AppConfig.SUPPORTED_LANGS
RENDER_CACHE_TIMEOUT = AppConfig.RENDER_CACHE_TIMEOUT


# ------- Jinja env global objects -------
app.jinja_env.globals["get_locale"] = get_locale
app.jinja_env.globals["SUPPORTED_LANGS"] = SUPPORTED_LANGS
app.jinja_env.globals["ANALYTICS_TAG_ID"] = AppConfig.ANALYTICS_TAG_ID
app.jinja_env.globals["RENDER_CACHE_TIMEOUT"] = RENDER_CACHE_TIMEOUT


# ------- Blueprint registry -------
app.register_blueprint(quiz_pages, subdomain="quiz")
app.register_blueprint(blog_pages, subdomain="blog")
app.register_blueprint(forum_pages, subdomain="forum")
app.register_blueprint(account_pages, subdomain="account")
app.register_blueprint(api, subdomain="api")
app.register_blueprint(database)
app.register_blueprint(redirects)


# ------- Locale selector -------
@app.route("/set-lang/<lang>", methods=["POST"])
def set_lang(lang):
    if lang in SUPPORTED_LANGS:
        debug_log.debug(f"[{request.remote_addr}] Changed language to [{lang}]")
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
    log.error(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [500 Error]")
    return render_template("errors/error_500.html"), 500


@app.errorhandler(werkzeug.exceptions.MethodNotAllowed)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def error405(error):
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [405 Error]")
    return render_template("errors/error_405.html"), 405


@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@cache.cached(timeout=RENDER_CACHE_TIMEOUT)
def template_error(error):
    log.critical(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}] that resulted in a [500 Template Error]")
    return render_template("errors/error_500.html"), 500


# ------- Before request -------
@app.before_request
def remove_www():
    if "://www." in request.url.lower():
        log.info(f"[{request.remote_addr}] Sent a request with [www.]")

        request_url = request.url.lower()
        return redirect(request_url.replace("www.", ""))


@app.before_request
def log_request():
    log.info(f"[{request.remote_addr}] Sent a [{request.method}] request to [{request.url}]")


# ------- Page routes -------
@app.route("/")
def index():
    posts = []
    posts.append(HomeNews("Placeholder post 1", "1980 mins", "img/carousel/placeholder.png", "#"))
    posts.append(HomeNews("Placeholder post 2", "2001 mins", "img/carousel/placeholder.png", "#"))
    posts.append(HomeNews("Placeholder post 3", "1963 mins", "img/carousel/placeholder.png", "#"))

    return render_template("index.html", page_views=Analytics.pageviews_this_month(), posts=posts)


@app.route("/mc-server")
def mc_server():
    # METHOD TESTS (TO BE REMOVED):
    js = JavaServer(java_servers[0])
    js = js.Status()
    
    print("=-=-=-=-=-= Java Edition Status method tests =-=-=-=-=-=")
    print(f"Java Status favicon_data: {js.favicon_data()}")
    print(f"Java Status max_players: {js.max_players()}")
    print(f"Java Status motd: {js.motd()}")
    print(f"Java Status opstat: {js.opstat()}")
    print(f"Java Status ping: {js.ping()}")
    print(f"Java Status players: {js.players()}")
    print(f"Java Status players_online: {js.players_online()}")
    print(f"Java Status raw_key: {js.raw_key('version')}")
    print(f"Java Status version: {js.version()}")
    print(f"Java Status raw: {js.raw()}")
    
    jq = JavaServer(java_servers[0])
    jq = jq.Query()
    
    print("")
    print("=-=-=-=-=-= Java Edition Query method tests =-=-=-=-=-=")
    print(f"Java Query map_name: {jq.map_name()}")
    print(f"Java Query max_players: {jq.max_players()}")
    print(f"Java Query motd: {jq.motd()}")
    print(f"Java Query players: {jq.players()}")
    print(f"Java Query players_online: {jq.players_online()}")
    print(f"Java Query raw_key: {jq.raw_key('version')}")
    print(f"Java Query software: {jq.software()}")
    print(f"Java Query raw: {jq.raw()}")
    
    bs = BedrockServer(bedrock_servers[0])
    bs = bs.Status()
    
    print("")
    print("=-=-=-=-=-= Bedrock Edition Status method tests =-=-=-=-=-=")
    print(f"Bedrock Status gamemode: {bs.gamemode()}")
    print(f"Bedrock Status max_players: {bs.max_players()}")
    print(f"Bedrock Status motd: {bs.motd()}")
    print(f"Bedrock Status opstat: {bs.opstat()}")
    print(f"Bedrock Status ping: {bs.ping()}")
    print(f"Bedrock Status map_name: {bs.map_name()}")
    print(f"Bedrock Status players_online: {bs.players_online()}")
    print(f"Bedrock Status version: {bs.version()}")
    # END METHOD TESTS.
    
    mods = []
    mods.append(MCMod("The Create mod", "https://example.com"))
    mods.append(MCMod("Flywheel", "https://example.com"))
    mods.append(MCMod("Securitycraft", "https://example.com"))
        
    players = js.players()
        
    servers = []
    servers.append(MCServer("The main Gigawhat modded 'Minecraft: Java Edition' survival server", "playmc.gigawhat.net", True, "Forge", "https://files.minecraftforge.net/net/minecraftforge/forge/index_1.18.2.html", mods, "https://example.com", js.players_online(), js.max_players(), players, js.opstat(), f"Java Edition {js.version()['name']}"))
        
    return render_template("mc_server.html", servers=servers)


@app.route("/privacy-policy")
def privacy_policy():
    return render_template("privacy_policy.html")


# ------- Running the app -------
if __name__ == "__main__":
    db.create_all()
    app.run()
