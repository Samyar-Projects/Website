#  Gigawhat Website Minecraft server util.
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
Minecraft server util.

Gets query and status information from a Minecraft server.
"""


# ------- Libraries and utils -------
from typing import Union, Any
from mcstatus import JavaServer, BedrockServer


# =+=+= Note: All methods return 0 or ERROR in case of an exception. =+=+=

# ------- Minecraft Java Edition server class -------
class JavaServer():
    def __init__(self, serv: JavaServer):
        global java_server
        java_server = serv
        

    # ------- Query class (Gets its information via query) -------
    class Query():
        def __init__(self):
            global java_q_res
            
            try:
                java_q_res = java_server.query()
                
            except Exception:
                java_q_res = None
            
        
        # ------- Usernames of players that are currently on the server -------
        def players(self) -> list:
            try:
                resp = []
                
                for player in java_q_res.players.names:
                    resp.append(player)
                
                return resp
            
            except Exception:
                return []
            

        # ------- Number of online players on the server -------
        def players_online(self) -> int:
            try:
                return java_q_res.players.online
            
            except Exception:
                return 0
        
        
        # ------- Number of maximum player slots -------
        def max_players(self) -> int:
            try:
                return java_q_res.players.max
            
            except Exception:
                return 0
            
            
        # ------- Server's Minecraft version/software information -------
        def software(self) -> dict:
            try:
                return {"name": java_q_res.software.version, "brand": java_q_res.software.brand, "plugins": java_q_res.software.plugins}
            
            except Exception:
                return {"name": "ERROR", "brand": "ERROR", "plugins": "ERROR"}
            
            
        # ------- Server's motd (Message of the day) -------
        def motd(self) -> str:
            try:
                return java_q_res.motd
            
            except Exception:
                return "ERROR"
            
            
        # ------- Name of the current server map -------
        def map_name(self) -> str:
            try:
                return java_q_res.map
            
            except Exception:
                return "ERROR"
            
            
        # ------- Get raw server response -------
        def raw(self) -> Union[dict, str]:
            try:
                return java_q_res.raw
            
            except Exception:
                return "ERROR"


    # ------- Status class (Gets its information via status) -------
    class Status():        
        def __init__(self):
            global java_s_res
            global java_opstatus
            
            try:
                java_opstatus = "ON"
                java_s_res = java_server.status()
                
            except ConnectionError:
                java_opstatus = "OF"
                java_s_res = None
                
            except OSError:
                java_opstatus = "OF"
                java_s_res = None
                
            except Exception:
                java_opstatus = "ERROR"
                java_s_res = None
        
        
        # ---- Server's operation status (ON = Online, OF = Offline) ----
        def opstat(self) -> str:       
            return java_opstatus
        
        
        # ------- Username and UUIDs of players that are currently on the server -------
        def players(self) -> list:
            try:
                resp = []
                
                for player in java_s_res.players.sample:
                    resp.append({"username": player.name, "uuid": player.id})
                    
                return resp
            
            except Exception:
                return []
            

        # ------- Number of online players on the server -------
        def players_online(self) -> int:
            try:
                return java_s_res.players.online
            
            except Exception:
                return 0
        
        
        # ------- Number of maximum player slots -------
        def max_players(self) -> int:
            try:
                return java_s_res.players.max
            
            except Exception:
                return 0
            
        
        # ------- Server's Minecraft version information -------
        def version(self) -> dict:
            try:
                return {"name": java_s_res.version.name, "protocol": java_s_res.version.protocol}
            
            except Exception:
                return {"name": "ERROR", "protocol": "ERROR"}
            
            
        # ------- Server's description/motd (Message of the day) -------
        def motd(self) -> str:
            try:
                return java_s_res.description
            
            except Exception:
                return "ERROR"
            
            
        # ------- Server's favicon image data -------
        def favicon_data(self) -> str:
            try:
                favicon = java_s_res.favicon
                
                if favicon:
                    return favicon
                
                raise Exception
            
            except Exception:
                return "ERROR"
            
            
        # ---- Server's ping latency ----
        def ping(self) -> float:
            try:
                return java_s_res.latency
                
            except Exception:
                return 0.000
            
            
        # ------- Get raw server response -------
        def raw(self) -> Union[Any, str]:
            try:
                return java_s_res.raw
            
            except Exception:
                return "ERROR"


# ------- Minecraft Bedrock Edition server class -------
class BedrockServer():
    def __init__(self, serv: BedrockServer):
        global bedrock_server
        bedrock_server = serv


    # ------- Status class (Gets its information via status) -------
    class Status():        
        def __init__(self):
            global bedrock_s_res
            global bedrock_opstatus
            
            try:
                bedrock_opstatus = "ON"
                bedrock_s_res = bedrock_server.status()
                
            except ConnectionError:
                bedrock_opstatus = "OF"
                bedrock_s_res = None
                
            except OSError:
                bedrock_opstatus = "OF"
                bedrock_s_res = None
                
            except Exception:
                bedrock_opstatus = "ERROR"
                bedrock_s_res = None
        
        
        # ---- Server's operation status (ON = Online, OF = Offline) ----
        def opstat(self) -> str:       
            return bedrock_opstatus
            

        # ------- Number of online players on the server -------
        def players_online(self) -> int:
            try:
                return bedrock_s_res.players_online
            
            except Exception:
                return 0
        
        
        # ------- Number of maximum player slots -------
        def max_players(self) -> int:
            try:
                return bedrock_s_res.players_max
            
            except Exception:
                return 0
    
        
        # ------- Server's Minecraft version information -------
        def version(self) -> dict:
            try:
                return {"name": bedrock_s_res.version.version, "protocol": bedrock_s_res.version.protocol, "brand": bedrock_s_res.version.brand}
            
            except Exception:
                return {"name": "ERROR", "protocol": "ERROR", "brand": "ERROR"}
            
            
        # ------- Server's description/motd (Message of the day) -------
        def motd(self) -> str:
            try:
                return bedrock_s_res.motd
            
            except Exception:
                return "ERROR"
            
        
        # ---- Server's ping latency ----
        def ping(self) -> float:
            try:
                return bedrock_s_res.latency
                
            except Exception:
                return 0.000


        # ------- Server's current gamemode -------
        def gamemode(self) -> str:
            try:
                gamemode = bedrock_s_res.gamemode
                
                if gamemode:
                    return gamemode
                
                raise Exception
            
            except Exception:
                return "ERROR"
            
            
        # ------- Name of the current server map -------
        def map_name(self) -> str:
            try: 
                map = bedrock_s_res.map
                
                if map:
                    return map
                
                raise Exception
            
            except Exception:
                return "ERROR"

