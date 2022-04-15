# Copyright 2022 Gigawhat Programming Team
# Helper function file.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
# LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

# ------- Libraries -------
import json
import re


# --- Translate message based on the lang.json file ---
def translate(key, lang):
    json_file = open("templates/" + lang + "/lang.json")
    data = json.load(json_file)
    return data[key]


# ------- Checkers -------

# --- Check e-mail validity ---
def check_email_validity(email):
    if email.__contains__("@") and email.__contains__(".") and email.__len__() < 50:
        return True
    
    return False
    
# --- Check password validity ---
def check_password_validity(password):
    if password.__len__() > 8 and re.search(r'\d', password) and re.match(r'\w*[A-Z]\w*', password) and password < 32:
        return True
    
    return False
