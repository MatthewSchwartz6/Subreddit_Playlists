# Subreddit_Playlists
Create a youtube playlist from your favorite music subreddit.

1. Create client_secret.json file for the Youtube Data Api. The steps are listed quite clearly at https://developers.google.com/youtube/v3/getting-started

2. Update the 'client_secrets' variable with the path to your client secret.

3. Make sure you have pip (python package manager), virtualenv, and git installed.

4. Once virtualenv is installed, create a 'virtual environment' for this project - type: `virtualenv Subreddit_Playlists`

5. Clone the repository -type: `git clone https://github.com/MatthewSchwartz6/Subreddit_Playlists.git`

6. Activate your virtual environment. type - `source bin/activate`

7. Install dependencies. type - `pip install -r requirements.txt`


Run: `python Subreddit_Playlists.py -h` for help.

Example session:

`python Subreddit_Playlists.py -l` - (gets a list of all music subreddits)`

`python Subreddit_Playlists.py -n liquiddnb -s new -t all -p 10`
