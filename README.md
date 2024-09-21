
# Post to Socials


##### Purpose

These are meant to ensure posting to the socials sites are easy.  Or at least standardized.
As new ones are implemented, they'll be added here.

Each one will have its own credentials.  I've included SAMPLE .json files in the /temp folder so you can see the formatting.



#### Credential Files

- BlueSky - BlueSky allows you to setup an application handle and password.  Its separate from your account credentials.  It's easily done in settings, and can be done via the web or app.
In my experience, I have never had an issue posting.
BlueSky has changed their image/video size limits over time, so keep an eye on those changes.

```
{
  "handle": "",
  "password": ""
}
```


- Twitter - Twitter has given me plenty of trouble over time.  Be ready for changes in this over time.
I will say that it is up to YOU to keep track of your daily posts.  While twitter indicates there's a limit, they no longer provide you with details in api calls.  
Through the post api's, twitter no longer indicates what your limit is, nor how many you have remaining.  In testing, no information changes in the information back to the user whether it is your first post, approaching the limit, or gone over.  The first indication you'll receive is a 429 error.
That said - I've found it to be 50 posts per 24 hour period.  The danger is that Twitter allows you to post more during a day, but doing so will cause the 429 error after an unknown number of posts.


```
{
  "client_id": "",
  "client_secret": "",
  "bearer_token": "",
  "Access Token": "",
  "Access Secret": ""
}
```

Currently, the free tier of twitter allows 50 posts per day.
If you've gone over the limit, your twitter project's application is locked out.  You'll be forced to create a new one with all new credentials.

As such, I've written the script to store the daily API count information in the credentials .json file.  Each time the script runs, it'll check the count.  If you've equaled your limit, the script WILL NO LONGER POST.
During normal script functionality, the credential file is updated with the current date and API count, starting at 0.


#### Social_Post_Logger class
Each media site has their own limits on the number of posts allowed.  This is keeping track of each one independently within a json file.
Your python script will import this and create a local variable.

```
import Social_Post_Logger                                            # Keeping track of rate limits

Rate_Limit = Social_Post_Logger.Social_Post_Logger()

```

During processing, you first check if you're allowed to post.  If true, then you're allowed.
```
if ( self.Rate_Limit.Can_Post_To_Social_Site( "Bluesky" ) ):
    self.Rate_Limit.Log_New_Post( "Bluesky" )
```

Each time Log_New_Post() is invoked, it writes the timestamp of the post.  This is the example of how the data is stored.

```
    "Bluesky": {
        "Daily Limit": 11666,
        "Posts": [
            "2024-08-05T13:29:23.016538",
            "2024-08-05T13:39:06.360154",
            "2024-08-05T13:48:09.884407",
            "2024-08-05T13:49:21.403318",
            "2024-08-05T13:58:47.463513",
            "2024-08-05T14:08:41.685199",
            "2024-08-05T14:10:34.753560",
            "2024-08-05T14:20:22.144756",
            "2024-08-06T09:50:34.446942",
            "2024-08-06T09:59:03.395232",
            "2024-08-06T10:08:02.207188",
            "2024-08-06T10:16:34.242119",
            "2024-08-06T10:26:29.164515",
            "2024-08-06T10:36:03.959431",
            "2024-08-06T10:44:18.858870",
            "2024-08-06T10:52:35.846912",
            "2024-08-06T11:01:36.786315",
            "2024-08-06T11:10:56.662972",
            "2024-08-06T11:20:38.635018",
            "2024-08-06T11:28:38.552865",
            "2024-08-06T12:36:51.465052",
            "2024-08-06T12:45:39.221595",
            "2024-08-06T12:54:56.197397"
        ]
    },

```
Can_Post_To_Social_Site() checks if the number of previously recorded posts are less than the daily limit.  It returns true if so, false otherwise.
As entries become older than 24 hours, they are removed from the storage.




### Usage

The scripts included here are made into classes.  So you can include them into a separate script.

```
import Post_Twitter                                                  # Allow to post to twitter
import Post_BlueSky                                                  # Allow to post to BlueSky
```

- BlueSky - here is an example function using the BlueSky class.
```


    def BlueSky( self, Text, Image_Path=None ):
        Max_Size = 1000000
        try:
            Bot = Post_BlueSky.Post_Content()   #Post_Twitter.Post_Content()
            args = Bot.Build_Args()

            if ( Text ):
                args.text = Text 
            if ( Image_Path ):
                # BlueSky now limiting file sizes to 1mb
                File_Size = os.path.getsize( Image_Path )
                if ( File_Size <= Max_Size ):
                    args.image.append( Image_Path )
                else:
                    self.Logger.Log( "Provided Image is too large for BlueSKy and won't be used in the post", "Warning" )
            
            Status = Bot.create_post( args )
            if ( Status is None ):
                return True
            else:
                self.Logger.Log( f"{Status}", "Debug" )
                return False
            
        except Exception as e:
            self.Logger.Log( f"\n\t**Encountered an error in BlueSky()**\n\t{str(e)}", "Error" )
            return False


```

- Twitter - here is an example function using the Twitter class.
```

    #---------------------------------------------------------------------------------------------------------------#
    # Function to Check and Update API Call Count
    # If it's a new day, reset the day and count, then save to the Credential file.  
    # Returns True if it can tweet.  False if not.
    #---------------------------------------------------------------------------------------------------------------#
    def Post( self, Text ):

        if ( len( Text ) > self.Character_Limit ):
            self.Logger.Log( f"Tweet Text too long.  Failed to Post: {e}", "Error" )
            return False


        if ( self.Rate_Limit.Can_Post_To_Social_Site( "Twitter" ) ):

            try:
                if ( len( self.Media_IDs ) > 0 ):
                    Post_Response = self.Client.create_tweet( text=Text, media_ids=self.Media_IDs )
                    #self.Logger.Log( f"DEBUGGING ONLY - self.Client.create_tweet() - media: {self.Media_IDs}", "Debug" )
                else:
                    Post_Response = self.Client.create_tweet( text=Text )
                    #self.Logger.Log( f"DEBUGGING ONLY - self.Client.create_tweet() - no media", "Debug" )
            
                ID = Post_Response.data['id']
                self.Media_IDs.clear()
                self.Rate_Limit.Log_New_Post( "Twitter" )
                return ID

            except Exception as e:
                self.Logger.Log( f"Tweet Failed to Post: {e}", "Error" )
                return False

        else:
            return False
                    
            

    #---------------------------------------------------------------------------------------------------------------#
    # Verifies valid media before uploading and adding to the Media ID list
    #---------------------------------------------------------------------------------------------------------------#
    def Add_Media( self, Media_Path ):
        try:

            if ( self.Rate_Limit.Can_Post_To_Social_Site( "Twitter" ) ):
                # Under the limit
                if ( os.path.exists( Media_Path ) ):
                    File_Size = os.path.getsize( Media_Path )
                    _, File_Extension = os.path.splitext( Media_Path )
                    if ( File_Extension.lower() in self.Images ):
                        if ( File_Size > self.TWITTER_IMAGE_SIZE_LIMIT ):
                            self.Logger.Log( f"Media file size ({File_Size / 1024 / 1024:.2f}MB) exceeds Twitter's size limit", "Warning" )
                        else:
                            Media = self.API.media_upload( filename=Media_Path )
                            self.Media_IDs.append( Media.media_id )
                            #self.Logger.Log( f"Media: {Media}" )
                    elif ( File_Extension.lower() in self.Movies ):
                        if ( File_Size > self.TWITTER_VIDEO_SIZE_LIMIT ):
                            self.Logger.Log( f"Media file size ({File_Size / 1024 / 1024:.2f}MB) exceeds Twitter's size limit", "Warning" )
                        else:
                            Media = self.API.media_upload( filename=Media_Path )
                            self.Media_IDs.append( Media.media_id )
                            self.Logger.Log( f"Media: {Media}" )
                    else:
                        self.Logger.Log( f"Media file type unsupported - {File_Extension}", "Warning" )

                else: 
                    self.Logger.Log( f"Media file not found: {Media_Path}", "Warning" )

                # Increasing the social logging for image uploads +1 - it has been unclear if twitter counts the image as a post within its limit
                #self.Rate_Limit.Log_New_Post( "Twitter" )
                return True
            
            else:
                self.Logger.Log( f"Exceeded rate limit, not posing.", "Error" )
                return False

        except Exception as e:
            self.Logger.Log( f"Encountered an error in Add_Media():\n{e}", "Error" )
            return False
        
```

Additionally, you may update the main start of Post_Twitter.py.  I was using this as testing for a post with just text, a post with an image, and a post with a movie.

```
    Posting = Post_Content()
    Current_Time = datetime.now().strftime("%H:%M:%S")

    Test = Posting.Post( f"API Testing - {Current_Time}" )

    time.sleep( 2 )
    Posting.Add_Media( r"d:\Data\Pics\temp\IMG_8524.PNG" )
    Current_Time = datetime.now().strftime("%H:%M:%S")
    Test = Posting.Post( f"API Testing - {Current_Time}" )
    time.sleep( 2 )
    
    Posting.Add_Media( r"d:\Data\Pics\temp\IMG_6791.MOV" )
    Current_Time = datetime.now().strftime("%H:%M:%S")
    Test = Posting.Post( f"API Testing - {Current_Time}" )
```


### Requirements
- BlueSky
```
import sys
import os                                                            # used to interact with the file system
import json                                                          # Interacts with json data
import argparse                                                      # used for easy parsing script input parametesr

import re
from typing import Dict, List
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
```

- Twitter
```
import tweepy                                                        # Ability to tweet
import os                                                            # interact with the OS
import json                                                          # Interacts with json data

import time                                                          # Working with time
from datetime import datetime                                        # Getting current time

from rich import print                                               # formatted / colored printing
from Logger import CustomLogger
```

