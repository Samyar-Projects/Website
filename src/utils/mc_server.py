#  Gigawhat Website Minecraft server util.
#  Copyright 2022 Gigawhat Programming Team
#  Written by Samyar Sadat Akhavi, 2020 - 2022.
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
from typing import Union
from init import mcserver


# ------- Query class (Gets its information via query) -------
class Query():
    # ------- Server's operation status (ON = Online, OF = Offline, ST = Starting) -------
    def opstat() -> str:
        try:
            mcserver.ping()
            return "ON"
        
        except ConnectionRefusedError:
            return "OF"
        
        except OSError:
            return "ST"
        
        
    # ------- Usernames of players that are currently on the server -------
    def players() -> Union[list, bool]:
        try:
            data = mcserver.query()
            resp = []
            
            for player in data.players.names:
                resp.append(player)
            
            return resp
        
        except Exception:
            return False
        

    # ------- Number of online players on the server -------
    def players_online() -> Union[int, bool]:
        try:
            data = mcserver.query()
            return data.players.online
        
        except Exception:
            return False
    
    
    # ------- Number of maximum player slots -------
    def max_players() -> Union[int, bool]:
        try:
            data = mcserver.query()
            return data.players.max
        
        except Exception:
            return False
        
        
    # ------- Server's Minecraft version -------
    def version() -> Union[str, bool]:
        try:
            data = mcserver.query()
            return data.software.version
        
        except Exception:
            return False
        
        
    # ------- Server's motd (Message of the day) -------
    def motd() -> Union[str, bool]:
        try:
            data = mcserver.query()
            return data.motd
        
        except Exception:
            return False
    
    
    # ------- Get information from the raw server response -------
    def raw(key: str) -> Union[str, list, int, bool]:
        try:
            data = mcserver.query()
            return data.raw[key]
        
        except Exception:
            return False


# ------- Status class (Gets its information via status) -------
class Status():
    # ------- Server's operation status (ON = Online, OF = Offline, ST = Starting) -------
    def opstat() -> str:
        try:
            mcserver.ping()
            return "ON"
        
        except ConnectionRefusedError:
            return "OF"
        
        except OSError:
            return "ST"
        
        
    # ------- Username and UUIDs of players that are currently on the server -------
    def players() -> Union[list, bool]:
        try:
            data = mcserver.status()
            resp = []
            
            for player in data.players.sample:
                resp.append({"username": player.name, "uuid": player.id})
                
            return resp
        
        except Exception:
            return False
        

    # ------- Number of online players on the server -------
    def players_online() -> Union[int, bool]:
        try:
            data = mcserver.status()
            return data.players.online
        
        except Exception:
            return False
    
    
    # ------- Number of maximum player slots -------
    def max_players() -> Union[int, bool]:
        try:
            data = mcserver.status()
            return data.players.max
        
        except Exception:
            return False
        
    
    # ------- Server's Minecraft version -------
    def version() -> Union[str, bool]:
        try:
            data = mcserver.status()
            return data.version.name
        
        except Exception:
            return False
        
        
    # ------- Server's description/motd (Message of the day) -------
    def motd() -> Union[str, bool]:
        try:
            data = mcserver.status()
            return data.description
        
        except Exception:
            return False
        

    # ------- Get information from the raw server response -------
    def raw(key: str) -> Union[str, list, int, bool]:
        try:
            data = mcserver.status()
            return data.raw[key]
        
        except Exception:
            return False

