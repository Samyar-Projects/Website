<h1 align="center">The Gigawhat website</h1>
<p align="center">
  	<a href="https://discord.gg/rMq7GujUZJ">Discord (WIP)</a>
	  |
  	<a href="https://gigawhat.net">Website (WIP)</a>
  	<br>
	<br>
	<a href="https://github.com/Gigawhat-net/Gigawhat-Website/actions/workflows/codeql-analysis.yml"><img src="https://github.com/Gigawhat-net/Gigawhat-Website/actions/workflows/codeql-analysis.yml/badge.svg"></a>
	|
	<a href="https://github.com/Gigawhat-net/Gigawhat-Website/blob/dev/LICENSE"><img src="https://img.shields.io/github/license/Gigawhat-net/Gigawhat-Website?color=blue"></a>
	|
	<a href="https://github.com/Gigawhat-net/Gigawhat-Website/issues"><img src="https://img.shields.io/github/issues/Gigawhat-net/Gigawhat-Website"></a>
	|
	<a href="https://github.com/SamKirkland/FTP-Deploy-Action"><img src="https://img.shields.io/badge/Deployed With-FTP DEPLOY ACTION-%3CCOLOR%3E?style=flat&color=d00000"></a>
	<br><br>
</p>

----
### Disclaimer: Website is still in development.

<br>

The Gigawhat website,<br>
Written in HTML 5, CSS 3, Bootstrap 5, and Python Flask.

Live website: https://gigawhat.net/

## How to run localy :
	1. Install the dependencies that are listed in the requirements.txt file.
	2. Add this to your hosts file (replace COMPUTERS_LOCAL_IP with your computer's local IP address) *1:
	     COMPUTERS_LOCAL_IP       gigawhat-local.gtw
	     COMPUTERS_LOCAL_IP       www.gigawhat-local.gtw
	     COMPUTERS_LOCAL_IP       quiz.gigawhat-local.gtw
	     COMPUTERS_LOCAL_IP       blog.gigawhat-local.gtw
	     COMPUTERS_LOCAL_IP       account.gigawhat-local.gtw
	     COMPUTERS_LOCAL_IP       api.gigawhat-local.gtw
	
	3. In the config.py file, change AppConfig(ProductionConfig) to AppConfig(LocalConfig)
	4. Create a vars.env file in the same directory as the config.py file and add these to the file (change the values to your own values):
	     FLASK_SECRET_KEY = "A VERY SECRET STRING"
	     PASSWORD_ENCRYPT_SALT = "A VERY SECRET SALT"
	     FLASK_MAIL_USERNAME = "SOME USERNAME"
	     FLASK_MAIL_PASSWORD = "A SECRET PASSWORD"
	
	5. Run the application with: python app.py
	6. Go to: http://gigawhat-local.gtw:5000/


	*1: If you don't know how to modify your hosts file, take a look at this guide: https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/
	Note: Python 3.7.12 is recommended.

## Support :
You can contact us via e-mail.<br>
E-mail: support.gpt@gigawhat.net
<br>
<br>
If you think that you have found a bug please report it <a href="https://github.com/Gigawhat-net/Gigawhat-Website/issues">here</a>.

<br>

## Contributing :

Please take a look at <a href="https://github.com/Gigawhat-net/Gigawhat-Website/blob/dev/CONTRIBUTING.md">CONTRIBUTING.md</a> for contributing.

<br>

## Credits :

| Role           | Name                                                             |
| -------------- | ---------------------------------------------------------------- |
| Lead Developer | <a href="https://github.com/samyarsadat">Samyar Sadat Akhavi</a> |
| Translation    | Rüzgar Kaya                                                      |
| Assets         | Rüzgar Kaya                                                      |

<br>
<br>

Copyright © 2021-2022 Gigawhat Programming Team.

