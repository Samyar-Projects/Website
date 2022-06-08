#  Gigawhat Website JSON models file.
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

"""JSON models for the Gigawhat website.

"""


# ------- JSON models -------

# -=-=-= Quiz player info =-=-=-
# ---- Model class ----
class QuizPlayerInfo():
    username: str
    with_account: bool
    right_answ: int
    wrong_answ: int

    def __init__(self, username: str, with_account: bool, right_answ: int, wrong_answ: int):
        self.username = username
        self.with_account = with_account
        self.right_answ = right_answ
        self.wrong_answ = wrong_answ


# ---- Convert model to a JSON serializable object ----
def player_info_json(player_info: QuizPlayerInfo) -> dict:
    json_data = {"username": player_info.username, "with_account": player_info.with_account, "right_answ": player_info.right_answ, "wrong_answ": player_info.wrong_answ}
    return json_data


# -=-=-= Home page news =-=-=-
# ---- Model class ----
class HomeNews():
    title: str
    read_dur: str
    thumb_url: str
    url: str

    def __init__(self, title: str, read_dur: str, thumb_url: str, url: str):
        self.title = title
        self.read_dur = read_dur
        self.thumb_url = thumb_url
        self.url = url
        
        
# -=-=-= Home page news =-=-=-
# ---- Model class ----
class MCMod():
    title: str
    link: str

    def __init__(self, title: str, link: str):
        self.title = title
        self.link = link


# -=-=-= Minecraft server =-=-=-
# ---- Model class ----
class MCServer():
    desc: str
    ip: str
    modded: bool
    modloader: str
    modloader_link: str
    mods: list
    mods_zip: str
    p_online: int
    p_total: int
    players: list
    stat: str
    version: str

    def __init__(self, desc: str, ip: str, modded: bool, modloader: str, modloader_link: str, mods: list, mods_zip: str, p_online: int, p_total: int, players: list, stat: str, version: str):
        self.desc = desc
        self.ip = ip
        self.modded = modded
        self.modloader = modloader
        self.modloader_link = modloader_link
        self.mods = mods
        self.mods_zip = mods_zip
        self.p_online = p_online
        self.p_total = p_total
        self.players = players
        self.stat = stat
        self.version = version