#  Gigawhat Website helper functions.
#  Copyright 2022 Gigawhat Programming Team
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
import json
import re


# --- Translate message based on the lang.json file ---
def translate(key, lang):
    json_file = open("templates/" + lang + "/lang.json")
    data = json.load(json_file)
    return data[key]


# --- Condition raw output from db query for quiz ---
def quiz_query_cond(query):
    query = query[0] 
    query = str(query)
    query = query.replace("<script", "")
    query = query.replace("</script", "")
    
    return query


# ------- Checkers -------

# --- Check e-mail validity ---
def check_email_validity(email):
    if "@" in email and "." in email and len(email) < 50:
        return True
    
    return False
    
# --- Check password validity ---
def check_password_validity(password):
    if len(password) > 8 and re.search(r"\d", password) and re.match(r"\w*[A-Z]\w*", password) and len(password) < 32:
        return True
    
    return False
