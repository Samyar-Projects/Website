#  Gigawhat Website application init file.
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


# ------- Libraries -------
import logging
from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
from mailjet_rest import Client
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from config import AppConfig
from mcstatus import JavaServer, BedrockServer


# ------- Flask and Flask plug-in init -------
app = Flask(__name__)
app.config.from_object(AppConfig)
cache = Cache(app)
db = SQLAlchemy(app)
babel = Babel(app)
csrf = CSRFProtect(app)
mailjet = Client(auth=(AppConfig.MAILJET_API_KEY, AppConfig.MAILJET_API_SECRET), version="v3.1")
ga = BetaAnalyticsDataClient()
mcserver = JavaServer(AppConfig.MC_SERVER_IP, AppConfig.MC_SERVER_PORT, 1)
mcbserver = BedrockServer.lookup("geyser.pixelblockmc.com")


# ------- Logging init -------
formatter = logging.Formatter("[%(asctime)s] [%(threadName)s/%(levelname)s] [%(module)s/%(funcName)s]: %(message)s")

# ---- Get a logger with custom settings ----
def get_logger(name, log_file, level):
    handler = logging.FileHandler(AppConfig.LOG_FILE_PATH + log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


log = get_logger("main", "GigawhatApp_MainPyLog.log", AppConfig.LOG_LEVEL)
debug_log = get_logger("debug", "GigawhatApp_DebugPyLog.log", logging.DEBUG)