# Vigie
<img src="/static/Media/Logo%20Vigie.svg" alt="logo for Vigie" title="Vigie" width="25%" align="right"/>
Social media bot project - Local webapp

## Functions
* post content on multiple plateform

## Objectives finals
* gather data around your content
* gather sociales at one place to prevent waste of time
* manage your scraped data localy
* alerts who is talking about your content

## Resources
* API Twitter [:ledger:](https://developer.twitter.com/en/products/twitter-api)
* API Reddit [:ledger:](https://www.reddit.com/prefs/apps)
  * script (To use reddit post create a personal use script)

## Installation
1. get source code 
2. Setup:
   - have python3 and pip installed on your computer/serve [:snake:](https://cloud.google.com/python/docs/setup)
     - go to `requirements.txt` in source code and setup your dev environement for the server (recommend via VScode after installing python3)
       - to launch the python dev environement to folder in terminal and use following cmd:
         - Windows: `.\env\Scripts\activate.ps1`
         - Linux/macOS: `source env/bin/activate`
   - or launch dockerfile
3. Run `flask run` in terminal(.env) inside your app folder
4. Go to (http://127.0.0.1:5000)
5. Register/Login a user account
6. Setup API 
   - go to ressource API of your choice
   - them input your credentials (http://127.0.0.1:5000/api)
7. Use the current app as you please and add features if you think you can make it better :octocat:

## Config for now
* Access API page
  * add your differents keys inside of it
