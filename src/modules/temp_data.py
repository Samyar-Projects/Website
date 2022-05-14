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


# ------- Libraries and utils -------
import json
from flask import Blueprint
from config import AppConfig
from init import log


# ------- Blueprint init -------
temp_data = Blueprint("temp_data", __name__)


# ------- Storage models -------

# ---- Quiz result storage ----
class QuizResultTemp():
    right_answ: int
    wrong_answ: int
    quiz_id: int

    def __init__(self, right_answ, wrong_answ, quiz_id):
        self.right_answ = right_answ
        self.wrong_answ = wrong_answ
        self.quiz_id = quiz_id


# ------- Read, write and delete -------

# ---- Quiz result storage ----
def read_quiz_res_temp(quiz_id: int):
    try:
        with open(f"{AppConfig.TEMPORARY_FILE_DIR}/quiz_result_temp.json", "r") as file:
            data = json.load(file)

        data = data[str(quiz_id)]
        to_send = QuizResultTemp(data["r_answ"], data["w_answ"], str(quiz_id))

    except Exception:
        log.exception(f"TemporaryDataError")
        return False

    else:
        return to_send


def write_quiz_res_temp(quiz_result_temp: QuizResultTemp):
    json_data = {quiz_result_temp.quiz_id: {"r_answ": quiz_result_temp.right_answ, "w_answ": quiz_result_temp.wrong_answ}}

    try:
        with open(f"{AppConfig.TEMPORARY_FILE_DIR}/quiz_result_temp.json", "r") as file:
            data = json.load(file)

        data.update(json_data)

        with open(f"{AppConfig.TEMPORARY_FILE_DIR}/quiz_result_temp.json", "w") as file:
            json.dump(data, file, indent=4)

    except Exception:
        log.exception(f"TemporaryDataError")
        return False

    else:
        return True


def delete_quiz_res_temp(quiz_id: int):
    try:
        with open(f"{AppConfig.TEMPORARY_FILE_DIR}/quiz_result_temp.json", "r") as file:
            data = json.load(file)

        data.pop(str(quiz_id))

        with open(f"{AppConfig.TEMPORARY_FILE_DIR}/quiz_result_temp.json", "w") as file:
            json.dump(data, file, indent=4)

    except Exception:
        log.exception(f"TemporaryDataError")
        return False

    else:
        return True
