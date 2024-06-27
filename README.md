# happy_fox_assignment


Automation Script Documentation

Link for Video Demo: https://drive.google.com/file/d/1icz7t59QfLrXDmh2Qe_RKRIbr6jlndtp/view?usp=sharing

Installation:
Clone this repository from GitHub:
git clone https://github.com/mohammedyusufshaikh/happy_fox_assignment
Install the required Python dependencies:
pip3 install -r requirements.txt


Enable the Gmail API for your Google account by following the instructions in the Google API Console (https://console.developers.google.com/).
Obtain credentials (client_secret.json) rename it to credentials.json for accessing the Gmail API and place it in the project directory.

Configuration:
Configure database connections in config.py
Configure rules in the rules.json file in the project directory.

Note:
MySQL on system is required and creation of database and table as well

Script to execute in order:
1] fetch_and_insert_mail.py
2] rule_based_action_on_mail.py


Scope of Improvements:

1] add more test cases
2] rules builder if more complex capability is required