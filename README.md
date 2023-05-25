# Vigie
<img src="/static/Media/Logo_Vigie.svg" alt="logo for Vigie" title="Vigie" width="25%" align="right"/>
Social media bot project - Local webapp

## Functions
* post content on multiple plateform

## Objectives finals
* gather data around your content
* gather sociales at one place to prevent waste of time
* manage your scraped data localy
* alerts who is talking about your content
* add fermet to hash json inside database

## Resources
* API Twitter [:ledger:](https://developer.twitter.com/en/products/twitter-api)
* API Reddit [:ledger:](https://www.reddit.com/prefs/apps)
  * script (To use reddit post create a personal use script)

## Installation
1. Get source code 
2. Setup:
   - have python3 and pip installed on your computer/serve [:snake:](https://cloud.google.com/python/docs/setup)
     - go to `requirements.txt` in source code and setup your dev environement for the server (recommend via VScode after installing python3)
       - to launch the python dev environement to folder in terminal and use following cmd:
         - Windows: `.\env\Scripts\activate.ps1`
         - Linux/macOS: `source env/bin/activate`
   - or launch dockerfile
3. Run `flask run` in terminal(.env) inside your app folder
4. Go to http://127.0.0.1:5000
5. Register/Login a user account
6. Setup API 
   - go to ressource API of your choice
   - them input your credentials http://127.0.0.1:5000/api
7. Use the current app as you please and add features if you think you can make it better :octocat:

## Config for now
* Access API page
  * add your differents keys inside of it


## Git hide database update
If you want to keep the `vigie.db` file in your repository but prevent it from being updated, you can use `git update-index --assume-unchanged vigie.db`. This will tell Git to temporarily ignore changes to the `vigie.db` file. The file will remain in the repository and will not be updated until you run `git update-index --no-assume-unchanged vigie.db` to start tracking changes again.

Please note that this is a local setting and will only apply to your local repository. Other users who clone the repository will still see changes to the `vigie.db` file unless they also run the `git update-index --assume-unchanged` command.