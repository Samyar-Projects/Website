#  Gigawhat Website temporary data storage module.
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
Temporary data storage module for the Gigawhat website.

Notes
-----
This module stores the temporary data in JSON files based on
storage models.
"""


# ------- Libraries and utils -------
import json
from config import AppConfig
from init import log
from typing import Union


# ------- Global variables -------
TEMPORARY_FILE_DIR = AppConfig.TEMPORARY_FILE_DIR


# ------- Storage models -------

# ---- Singleplayer quiz result storage ----
class SpQuizResultTemp():
    right_answ: int
    wrong_answ: int
    quiz_id: int

    def __init__(self, right_answ, wrong_answ, quiz_id):
        self.right_answ = right_answ
        self.wrong_answ = wrong_answ
        self.quiz_id = quiz_id


# ------- Read, write and delete -------

# -=-=-= Singleplayer quiz result storage =-=-=-
# ---- Read quiz results from temporary storage ----
def read_sp_quiz_res_temp(quiz_id: Union[int, str]) -> Union[SpQuizResultTemp, bool]:
    try:
        with open(f"{TEMPORARY_FILE_DIR}/sp_quiz_result_temp.json", "r") as file:
            data = json.load(file)

        data = data[str(quiz_id)]
        to_send = SpQuizResultTemp(data["r_answ"], data["w_answ"], str(quiz_id))
        
        return to_send

    except Exception:
        log.exception("TemporaryDataReadException")
        return False


# ---- Write quiz results to temporary storage ----
def write_sp_quiz_res_temp(quiz_result_temp: SpQuizResultTemp) -> bool:
    json_data = {quiz_result_temp.quiz_id: {"r_answ": quiz_result_temp.right_answ, "w_answ": quiz_result_temp.wrong_answ}}

    try:
        with open(f"{TEMPORARY_FILE_DIR}/sp_quiz_result_temp.json", "r") as file:
            data = json.load(file)

        data.update(json_data)

        with open(f"{TEMPORARY_FILE_DIR}/sp_quiz_result_temp.json", "w") as file:
            json.dump(data, file, indent=4)
            
        return True

    except Exception:
        log.exception("TemporaryDataWriteException")
        return False
        

# ---- Delete quiz results from temporary storage ----
def delete_sp_quiz_res_temp(quiz_id: Union[int, str]) -> bool:
    try:
        with open(f"{TEMPORARY_FILE_DIR}/sp_quiz_result_temp.json", "r") as file:
            data = json.load(file)

        data.pop(str(quiz_id))

        with open(f"{TEMPORARY_FILE_DIR}/sp_quiz_result_temp.json", "w") as file:
            json.dump(data, file, indent=4)
            
        return True

    except Exception:
        log.exception("TemporaryDataDeleteException")
        return False
        
