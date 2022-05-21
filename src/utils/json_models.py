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

    def __init__(self, username, with_account, right_answ, wrong_answ):
        self.username = username
        self.with_account = with_account
        self.right_answ = right_answ
        self.wrong_answ = wrong_answ


# ---- Convert model to a JSON serializable object ----
def player_info_json(player_info: QuizPlayerInfo):
    json_data = {"username": player_info.username, "with_account": player_info.with_account, "right_answ": player_info.right_answ, "wrong_answ": player_info.wrong_answ}
    return json_data


# -=-=-= Home page news =-=-=-
# ---- Model class ----
class HomeNews():
    title: str
    read_dur: str
    thumb_url: str
    url: str

    def __init__(self, title, read_dur, thumb_url, url):
        self.title = title
        self.read_dur = read_dur
        self.thumb_url = thumb_url
        self.url = url