
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
Through the post api's, twitter no longer indiciates what your limit is, nor how many you have remaining.  In testing, no infomration changse in the information back to the user whether it is your first post, approaching the limit, or gone over.  The first inidicate you'll receive is a 429 error.
```
{
  "client_id": "",
  "client_secret": "",
  "bearer_token": "",
  "Access Token": "",
  "Access Secret": "",
  "Date": "2024-07-07",
  "API_Tweet_Count": 9
}
```

Currently, the free tier of twitter allows 50 posts per day.
Notes - if you've gone over the limit, you are afforded a grace period.  But "too many" and your twitter project's application is locked out.  You'll be forced to create a new one with all new credentials.
Notes - If you've gone over the limit, you may still be allows to upload media, but you'll fail on the post itself.

As such, I've written the script to store the daily API count information in the credentials .json file.  Each time the script runs, it'll check the count.  If you've equaled your limit, the script WILL NO LONGER POST.
During normal script functionality, the credential file is updated with the current date and API count, starting at 0.



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
    def Twitter( self, Text, Image_Path=None ):
        try:

            Bot = Post_Twitter.Post_Content()
            
            if ( Image_Path ):
                Test = Bot.Add_Media( Image_Path )
                if ( not Test ):
                    raise ValueError( "Image failed to upload" )

            Status = Bot.Post( Text )

            if ( Status ):
                self.Logger.Log(f"Tweet posted successfully. Tweet ID: {Status}", "Debug")
                return True
            else:
                self.Logger.Log( f"Failed to post tweet.", "Error" )
                return False


        except Exception as e:
            self.Logger.Log( f"\n\t**Encountered an error in Twitter()**\n\t{str(e)}", "Error" )
```

Additionally, you may update the main start of Post_Twitter.py.  I was usingt his as testing for a post with just text, a post with an image, and a post with a movie.

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

