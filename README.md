# Subreddit_Playlists
Create youtube playlist from your favorite subreddit.


My favorite way to listen to music from reddit. 

This program runs on your command line(terminal or powershell). These steps are meant for people who might not have experience in this thing.

1. Create client_secret.json file for the Youtube Data Api. Add it to the project directory that you will create below.
The steps are listed quite clearly at https://developers.google.com/youtube/v3/getting-started

2. Make sure you have pip (python package manager) installed. pip or pip3 work. Type `which pip` to see if it is already installed. 

3. Make sure you have git installed for the command line.  Type `which git` to test.

4. Install virtual environment if you don't have it already - type: `pip install virtualenv`

5. Once virtualenv is installed, create a 'virtual environment' for this project - type: `virtualenv Subreddit_Playlists`

6. Go into the new Subreddit_Playlists folder by typing `cd /path/to/folder/Subreddit_Playlists`

7. Clone the repository: `git clone https://github.com/MatthewSchwartz6/Subreddit_Playlists.git`

8. Activate your virtual environment. type - `source bin/activate`

9. Install dependencies. type - `pip install requests bs4 google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2`


Run: `python Subreddit_Playlists.py -h` for help with the command line arguments.

Example session:

`python Subreddit_Playlists.py -l (gets a list of all music subreddits)`

`python Subreddit_Playlists.py -n liquiddnb -s new -t all -p 10`

A browser tab should open for your google validation.
Check your youtube channel after running and enjoy.
