# Subreddit_Playlists
Create youtube playlist from your favorite subreddit.


My favorite way to listen to music from reddit. 

There are a few things you need to do to get it set up:

1. Create client_secret.json file for the Youtube Data Api. 
The steps are listed quite clearly at https://developers.google.com/youtube/v3/getting-started

2. (For Python 3.x ) pip3 install requests bs4 google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2


*Unfortunately there seems to be a bandwith limit that I hope to solve in the future. The maximum amount of songs I've been able to insert into a youtube playlist is around 20. 

Run in your favorite shell: `python3 Subreddit_YT_Playlist.py --help` to see the argument options. 

*You will have to copy/paste a link in the browser to validate the request with your Google authentication. Then copy/paste the token back into the shell. Again, its a work in progress!

Check your youtube channel after running and enjoy.
