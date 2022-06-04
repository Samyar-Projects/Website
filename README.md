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
Written with HTML 5, CSS 3, Bootstrap 5, and Python Flask.

Live website: https://gigawhat.net/

## How to run localy :
1. Install the dependencies that are listed in the `requirements.txt` file.
2. Add this to your `hosts` file (replace `COMPUTERS_LOCAL_IP` with your computer's local IP address) *1:<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `gigawhat-local.gtw`<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `www.gigawhat-local.gtw`<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `quiz.gigawhat-local.gtw`<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `blog.gigawhat-local.gtw`<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `account.gigawhat-local.gtw`<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `api.gigawhat-local.gtw`<br>
	`COMPUTERS_LOCAL_IP` &nbsp;&nbsp;&nbsp;&nbsp; `forum.gigawhat-local.gtw`
	
3. In the `config.py` file, change `AppConfig(ProductionConfig)` to `AppConfig(LocalConfig)`
4. In the `config.py` file, change `ANALYTICS_TAG_ID` to your own Google Analytics G- ID. *2
5. In the `config.py` file, change `ANALYTICS_PROPERTY_ID` to your own Google Analytics property ID.
6. In the `config.py` file, change `MAILJET_API_KEY` and `MAILJET_API_SECRET` to your own Mailjet credentials. *3
7. Put your Google Service Account credentials JSON file in a folder called `secrets`. Create this folder in the same directory as the `app.py` file. (Rename the file to `ga_creds.json`) *4
8. Create a `vars.env` file in the `secrets` folder that you created and add these to it (change the values to your values):<br>
	`FLASK_SECRET_KEY = "A VERY SECRET STRING"`<br>
	`PASSWORD_ENCRYPT_SALT = "A VERY SECRET SALT"`<br>
	`FLASK_MAIL_USERNAME = "SOME USERNAME"`<br>
	`FLASK_MAIL_PASSWORD = "A SECRET PASSWORD"`<br>

9. Run the application with: `python app.py`
10. Go to: http://gigawhat-local.gtw:5000/


<br>
*1: If you don't know how to modify your hosts file, take a look at this guide: https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/<br>
<br>
*2: If you don't know how to get a Google Analytics tracking ID, take a look at this guide: https://support.google.com/analytics/answer/9304153?hl=en&ref_topic=9303319#zippy=%2Cfind-your-g--id-for-any-platform-that-accepts-a-g--id (NOTE: You will be creating the data stream for Web. In the 'Set up data collection' section, go down to 'Find your "G-" ID' then follow those steps and get your G- ID)<br>
<br>
*3: Create a Mailjet account, go to 'Account Settings > API Key Management' then create an API key.<br>
<br>
*4: To get this file, create a 'Google Cloud Platform' project, enable the 'Analytics Data API' in the project, go to the 'Credentials' section, create a 'Service Account' and finally go to the 'Keys' tab on your Service Account page then create and download a JSON key.<br>
<br>
Note: Python 3.7.12 is recommended.<br>
<br>

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

