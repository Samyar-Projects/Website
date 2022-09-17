#  Samyar Projects Website Minecraft server init file.
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


# ------- Libraries -------
from config import AppConfig
from modules.database import MinecraftServer
from mcstatus import JavaServer, BedrockServer
from init import db
from utils.temp_data import McServerLatestInfo


# ------- Global variables -------
java_servers = []
bedrock_servers = []


# ------- Minecraft server init function -------
def init_mc():
    # ------- Java Edition servers -------
    java_server_query = db.session.query(MinecraftServer).filter_by(edition="Java", status=True).all()

    for server in java_server_query:
        if server.port:
            mcjserver = JavaServer(server.ip_add, server.port, AppConfig.MC_SERVER_TIMEOUT)
        
        else:
            mcjserver = JavaServer.lookup(server.ip_add, AppConfig.MC_SERVER_TIMEOUT)
        
        # --- Add a temporary data entry if the server doesn't have an entry to prevent errors ---
        if not McServerLatestInfo.read(f"{server.ip_add}:{mcjserver.address.port}"):
            McServerLatestInfo("1.18.2", 20, f"{server.ip_add}:{mcjserver.address.port}").write()
        
        java_servers.append(mcjserver)


    # ------- Bedrock Edition servers -------
    bedrock_server_query = db.session.query(MinecraftServer).filter_by(edition="Bedrock", status=True).all()

    for server in bedrock_server_query:
        if server.port:
            mcbserver = BedrockServer(server.ip_add, server.port, AppConfig.MC_SERVER_TIMEOUT)
            
        else:
            mcbserver = BedrockServer.lookup(server.ip_add, AppConfig.MC_SERVER_TIMEOUT)
            
        # --- Add a temporary data entry if the server doesn't have an entry to prevent errors ---
        if not McServerLatestInfo.read(f"{server.ip_add}:{mcbserver.address.port}"):
            McServerLatestInfo("1.18.2", 20, f"{server.ip_add}:{mcbserver.address.port}").write()
            
        bedrock_servers.append(mcbserver)