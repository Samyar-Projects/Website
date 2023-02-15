#  Samyar Projects Website JSON models file.
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

"""JSON models for the Samyar Projects Website.

"""


# ------- JSON models -------

# -=-=-= Quiz player info =-=-=-
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
    def as_json(self) -> dict:
        return {"username": self.username, "with_account": self.with_account, "right_answ": self.right_answ, "wrong_answ": self.wrong_answ}


# -=-=-= Home page news =-=-=-
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