#!env/bin/python3

import os
import sys
import datetime
import argparse

import requests
from bs4 import BeautifulSoup

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow




class Subreddit_YT_Playlist:
    client_secrets_file = "client_secret.json"
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
        Command line program to convert a subreddit page into a youtube playlist.
        Must provide command line argument of the subreddit name.
        Type --help for more information
        """)
        
        #arguments:
        #mandatory - subreddit name
        #optional - navigation, time pref, page depth
        parser.add_argument("subreddit_name",help = "A valid subreddit name as a mandatory argument",)
        parser.add_argument("-s","--sorting",default = "hot",choices = ["hot","new"],help = "Each subreddit has its own sorting method. Only acceptable arguments: new or hot.")
        parser.add_argument("-t","--time",default = "week",choices = ["day","week","month", "year", "all"],help = "For the \"top\" sorting of the subreddit, you may also indicate additional time based arguments. Acceptable arguments: day, hour, week, month, year, all")
        parser.add_argument("-p","--page-depth",default=1,type=int,help="Integer. Amount of pages (with 25 posts per page) to go through. Anything over 10 pages will be shortened because come-on!")

        args = parser.parse_args()
        if (args.time):
            self.is_time = True
        self.subreddit_name = args.subreddit_name

        self.subreddit_nav = args.sorting
        self.subreddit_time_pref = args.time
        self.page_depth = args.page_depth

        return args
    def get_video_ids(self):
        #scrape subreddits for youtube links  and return array of video id's

        video_ids = []
        URL = []
        page_url = "https://www.reddit.com/r/"

        page_url += self.subreddit_name + "/" + self.subreddit_nav + "/"
        if (self.is_time): 
            if (self.subreddit_nav == "new"):
                page_url += "?sort=new&t=" + self.subreddit_time_pref
            elif (self.subreddit_nav == "hot"):
                page_url += "?sort=hot&t=" + self.subreddit_time_pref
        i = 0
        count = 25
        while (i<self.page_depth):
            if (i > 0):
                if (self.is_time):
                    nextPageStr = ("&count=" + str(count) + "&after=")
                else :
                    nextPageStr = ("?count=" + str(count) + "&after=")
                count +=25
                nextPageID = lastDiv['data-fullname']
                nextPage =  page_url + nextPageStr + nextPageID
                URL.append(nextPage)


            else :
                URL.append(page_url)

            print (URL[i])
            request = requests.get(URL[i],headers = {'User-agent':'your bot 0.1'})
            soup = BeautifulSoup(request.text,'html.parser')
            links = soup.find_all('div',attrs={'data-subreddit':self.subreddit_name})
            
            lastDiv = links[(len(links)-1)]
            print (lastDiv['data-fullname'])
            i+=1


            for link in links:
                music = link['data-url']
                if ((str(music)[:23]) == "https://www.youtube.com"):
                    video_ids.append((str(music)[32:43]))
                    #print (str(music)[32:43])

        return video_ids

    def get_authentication_services(self):

        flow = InstalledAppFlow.from_client_secrets_file(self.client_secrets_file, self.SCOPES)
        credentials = flow.run_console()
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
        print(response)

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

    def insert_items(self,client, properties,**kwargs):
      resource = self.build_resource(properties)

      kwargs = self.remove_empty_kwargs(**kwargs)

      response = client.playlistItems().insert(
        body=resource,
        **kwargs
      ).execute()

      return self.print_response(response)


if __name__ == '__main__':
  obj = Subreddit_YT_Playlist()
  args = obj.app_args()
  video_ids = obj.get_video_ids();


  os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
  client = obj.get_authentication_services()


  p_id = obj.make_playlist(client,args)



  for v_id in video_ids:
      obj.insert_items(client,
        {'snippet.playlistId': p_id,
         'snippet.resourceId.kind': 'youtube#video',
         'snippet.resourceId.videoId': v_id},
        part='snippet')
   
