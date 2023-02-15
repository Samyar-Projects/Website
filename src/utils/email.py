#  Samyar Projects Website Mailjet mailing API util.
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

"""
Mail util.

Sends emails with the Mailjet API.
"""


# ------- Libraries and utils -------
from flask import abort
from flask_security import MailUtil
from init import mailjet, debug_log, log
from typing import Union


# -=-=-= Mail util classes =-=-=-

# ---- Custom mail util for Flask-Security ----
class SecurityMailUtil(MailUtil):
    def send_mail(self, template: str, subject: str, recipient: str, sender: Union[str, tuple], body: str, html: str, user, **kwargs) -> None:
        mail_data = {
            "Messages":
            [{
                "From":
                {
                    "Email": sender,
                    "Name": "Samyar Projects Account"
                },
                    
                "To":
                [{
                    "Email": recipient
                }],
                
                "Subject": subject,
                "TextPart": body,
                "HTMLPart": html
            }]
        }

        result = mailjet.send.create(data=mail_data)
        debug_log.debug(f"Sent security mail, Mailjet responded with status code [{result.status_code}]")
        
        if result.status_code != 200:
            debug_log.debug(f"Attempted to send security mail but Mailjet responded with error code [{result.status_code}]")
            log.critical(f"Attempted to send security mail but Mailjet responded with error code [{result.status_code}]")
            abort(500)