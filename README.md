<h1 align="center">The Samyar Projects website</h1>
<p align="center">
  	<a href="https://gigawhat.net/discord">Discord</a>
	  |
  	<a href="https://gigawhat.net">Website (WIP)</a>
  	<br>
	<br>
	<a href="https://github.com/Samyar-Projects/Website/actions/workflows/codeql-analysis.yml"><img src="https://github.com/Samyar-Projects/Website/actions/workflows/codeql-analysis.yml/badge.svg"></a>
	|
	<a href="https://github.com/Samyar-Projects/Website/blob/dev/LICENSE"><img src="https://img.shields.io/github/license/Samyar-Projects/Website?color=blue"></a>
	|
	<a href="https://github.com/Samyar-Projects/Website/issues"><img src="https://img.shields.io/github/issues/Samyar-Projects/Website"></a>
	|
	<a href="https://github.com/SamKirkland/FTP-Deploy-Action"><img src="https://img.shields.io/badge/Deployed With-FTP DEPLOY ACTION-%3CCOLOR%3E?style=flat&color=d00000"></a>
	<br><br>
</p>

----
### Disclaimer: Website is still in development.
*Note:* **I am taking a break to work on my R.O.S. robot project thus development on all Samyar Projects projects will be paused for a little while. None of Samyar Projects's projects are canceled.**

<br>

The Samyar Projects website,<br>
Written with HTML 5, CSS 3, Bootstrap 5, and Python Flask.

Live website: https://gigawhat.net/

## How to run localy :
1. Install the dependencies that are listed in the `requirements.txt` file.
2. Add this to your `hosts` file *1:<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `sp-local.stw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `www.sp-local.stw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `quiz.sp-local.stw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `blog.sp-local.stw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `account.sp-local.stw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `api.sp-local.stw`<br>
	`127.0.0.1` &nbsp;&nbsp;&nbsp;&nbsp; `forum.sp-local.stw`
	
3. In the `config.py` file, change `AppConfig(ProductionConfig)` to `AppConfig(LocalConfig)`
4. In the `config.py` file, change `ANALYTICS_TAG_ID` to your own Google Analytics G- ID. *2
5. In the `config.py` file, change `ANALYTICS_PROPERTY_ID` to your own Google Analytics property ID.
6. Put your Google Service Account credentials JSON file in a folder called `secrets`. Create this folder in the same directory as the `app.py` file. (Rename the file to `ga_creds.json`) *3
7. Create a `vars.env` file in the `secrets` folder that you created and add these to it (change the values to your values) *4:<br>
	`FLASK_SECRET_KEY = "A VERY SECRET STRING"`<br>
	`PASSWORD_ENCRYPT_SALT = "A VERY SECRET SALT"`<br>
	`MAILJET_API_KEY = "MAILJET API KEY"`<br>
	`MAILJET_API_SECRET = "MAILJET API SECRET"`<br>

8. Run the application with: `python app.py`
9. Go to: http://sp-local.stw:5000/


<br>
*1: If you don't know how to modify your hosts file, take a look at this guide: https://www.howtogeek.com/howto/27350/beginner-geek-how-to-edit-your-hosts-file/<br>
<br>
*2: If you don't know how to get a Google Analytics tracking ID, take a look at this guide: https://support.google.com/analytics/answer/9304153?hl=en&ref_topic=9303319#zippy=%2Cfind-your-g--id-for-any-platform-that-accepts-a-g--id (NOTE: You will be creating the data stream for Web. In the 'Set up data collection' section, go down to 'Find your "G-" ID' then follow those steps and get your G- ID)<br>
<br>
*3: To get this file, create a 'Google Cloud Platform' project, enable the 'Analytics Data API' in the project, go to the 'Credentials' section, create a 'Service Account' and finally go to the 'Keys' tab on your Service Account page then create and download a JSON key.<br>
<br>
*4: To get the Mailjet credentials: Create a Mailjet account, go to 'Account Settings > API Key Management' then create an API key.<br>
<br>
Note: Python 3.7.12 is recommended.<br>
<br>

## Support :
If you think that you have found a bug please report it <a href="https://github.com/Samyar-Projects/Website/issues">here</a>.
<br>
<br>

## Contributing :
Please take a look at <a href="https://github.com/Samyar-Projects/Website/blob/dev/CONTRIBUTING.md">CONTRIBUTING.md</a> for contributing.
<br>
<br>

## Credits :

| Role           | Name                                                             |
| -------------- | ---------------------------------------------------------------- |
| Lead Developer | <a href="https://github.com/samyarsadat">Samyar Sadat Akhavi</a> |
| Translation    | Rüzgar Kaya                                                      |
| Assets         | Rüzgar Kaya                                                      |

<br>
<br>

Copyright © 2021-2022 Samyar Projects.

