#!env/bin/python3

import os
import sys
import datetime
import argparse
import time
import random

import requests
from bs4 import BeautifulSoup

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow


class Subreddit_YT_Playlist:
    client_secrets_file = ""
    SCOPES = ['https://www.googleapis.com/auth/youtube']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    subreddit_name = ""
    subreddit_nav = ""
    subreddit_time_pref = ""
    page_depth = 1
    is_time = False


    def app_args(self):
        parser = argparse.ArgumentParser(description="""
        Make a youtube playlist from the links found on the subreddit page of your choice.
        """)

        parser.add_argument("-n","--subreddit-name",help = "A valid subreddit name is a mandatory argument unless you use the \'-l\' option to list valid subreddit names.")
        parser.add_argument("-l","--list-valid-names",action="store_true",help = "Print the most common music subreddits.")
        parser.add_argument("-s","--sorting",default = "hot",choices = ["hot","new"],help = "Each subreddit has its own sorting method. Acceptable arguments: new or hot.")
        parser.add_argument("-r","--max-results",default=25,type=int,help="Integer. Max results to parse through. Note: Will only find youtube links.")


        args = parser.parse_args()
        valid_subreddits = self.get_valid_subreddits()

        if (args.subreddit_name == None):
            if (args.list_valid_names == None):
                print ("You must provide a subreddit name.")
                sys.exit()
            elif (args.list_valid_names):
                print ('\n'.join(valid_subreddits))
                sys.exit()

        self.subreddit_name = args.subreddit_name
        self.subreddit_nav = args.sorting
        self.max_results = args.max_results

        ##fIx miSTYpeD suBRedDit nAmES
        for subreddit in valid_subreddits:
            if (subreddit.upper() == self.subreddit_name.upper()):
                self.subreddit_name = subreddit

        return args

    def get_valid_subreddits(self):
        with open('music_subreddit_list.txt','r') as music_file:
            valid = music_file.readlines()
            valid = [v[:-1] for v in valid]
            return valid
            
    def get_video_ids(self):

        video_ids = []
        url = "https://gateway.reddit.com/desktopapi/v1/subreddits/{}?sort={}".format(self.subreddit_name,self.subreddit_nav)
        headers = {'User-agent':'Mozilla/5.0','Connection':'keep-alive'}
        response = requests.get(url,headers=headers)
        json = response.json()
        num_results = self.max_results / 25
        i = 0
        while (i < num_results):
            token = json['token']
            for postId in json['postIds']:
                try :
                    music_link = json['posts'][postId]['source']['url']
                    if ("youtube" in music_link and len(music_link)<=43):
                        video_ids.append(music_link[32:43])
                except TypeError:
                    print 'Whoops! Lost one due to nullness'
            next_url = url + "?after=" + token 
            response = requests.get(next_url,headers=headers)
            json = response.json()
            i += 1

        difference = len(video_ids) - self.max_results
        if (difference  > 0):
            difference *= -1
            video_ids = video_ids[:difference]

        return video_ids

    def get_authentication_services(self):

        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.SCOPES)      
        credentials = flow.run_local_server()
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials = credentials)

    def make_playlist(self,youtube,args):
        todayBox = []
        date = datetime.date.today()
        todayBox.append(date)
        title = self.subreddit_name + "-" + self.subreddit_nav + "-" + str(todayBox[0])
        descr = "A playlist made from the " + self.subreddit_name + " subreddit on " + str(todayBox[0])
        body = dict(
        snippet=dict(
          title=title,
          description=descr
        ),
        status=dict(
          privacyStatus='private'
                    )
        )

        playlists_insert_response = youtube.playlists().insert(
        part='snippet,status',
        body=body
        ).execute()

        print ('New playlist ID: %s' % playlists_insert_response['id'])
        return playlists_insert_response['id']

    def print_response(self,response):

        print('Video Added: %s\n' % response['snippet']['title'])

    def build_resource(self,properties):

      resource = {}
      for p in properties:
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
          is_array = False
          key = prop_array[pa]

          if key[-2:] == '[]':
            key = key[0:len(key)-2:]
            is_array = True

          if pa == (len(prop_array) - 1):
            if properties[p]:
              if is_array:
                ref[key] = properties[p].split(',')
              else:
                ref[key] = properties[p]
          elif key not in ref:
            ref[key] = {}
            ref = ref[key]
          else:
            ref = ref[key]
      return resource

    def remove_empty_kwargs(self,**kwargs):

      good_kwargs = {}
      if kwargs is not None:
        for key, value in kwargs.items():
          if value:
            good_kwargs[key] = value
      return good_kwargs

    def insert_song(self,client, properties,**kwargs):

        resource = self.build_resource(properties)
        kwargs = self.remove_empty_kwargs(**kwargs)
        for i in range(0,5):
            try:
                response = client.playlistItems().insert(
                body=resource,
                **kwargs
                ).execute()
                return self.print_response(response)
            except HttpError as error:
                if error.resp.reason in ['userRateLimitExceeded', 'quotaExceeded','internalServerError','backendError']:
                    time.sleep((2**n) + random.random())
                else:
                    print ('Reason for not uploading to playlist:\n')
                    print (error.resp.reason)
                    break

if __name__ == '__main__':
  youtube_playlist = Subreddit_YT_Playlist()
  args = youtube_playlist.app_args()
  video_ids = youtube_playlist.get_video_ids();

  print video_ids
  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = youtube_playlist.get_authentication_services()

  playlist_id = youtube_playlist.make_playlist(client,args)

  for v_id in video_ids:
      youtube_playlist.insert_song(client,
      {'snippet.playlistId': playlist_id,
      'snippet.resourceId.kind': 'youtube#video',
      'snippet.resourceId.videoId': v_id},
      part='snippet')
