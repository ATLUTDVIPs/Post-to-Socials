

#---------------------------------------------------------------------------------------------------------------#
# Load Modules
# py -m pip install --upgrade package_name
#---------------------------------------------------------------------------------------------------------------#
import tweepy                                                        # Ability to tweet
import os                                                            # interact with the OS
import json                                                          # Interacts with json data

import time                                                          # Working with time
from datetime import datetime                                        # Getting current time

from rich import print                                               # formatted / colored printing
from Logger import CustomLogger

import Social_Post_Logger                                            # Keeping track of rate limits


#---------------------------------------------------------------------------------------------------------------#
# Defining the Class
#---------------------------------------------------------------------------------------------------------------#
class Post_Content( ):
    CREDENTIALS_FILE = r'D:\Data\git\Credentials_Twitter_ATLUTD.json'
    Rate_Limit = Social_Post_Logger.Social_Post_Logger()

    Consumer_Key = ""
    Consumer_Secret = ""
    Access_Token = ""
    Access_Token_Secret = ""

    Authorization = None
    Client        = None
    API           = None

    TWITTER_IMAGE_SIZE_LIMIT = 5 * 1024 * 1024    # 5MB in bytes
    TWITTER_VIDEO_SIZE_LIMIT = 512 * 1024 * 1024  # 512MB in bytes

    Media_IDs = []  # List to hold multiple media ID's

    Images = [ '.jpg', '.jpeg', '.png', '.gif' ]
    Movies = [ '.mov', '.mpg' ]

    Character_Limit = 280


    #---------------------------------------------------------------------------------------------------------------#
    # Class initialization
    #---------------------------------------------------------------------------------------------------------------#
    def __init__ ( self ):
        self.Logger = CustomLogger( __file__, "Debug" )
        self.Set_Credentials()
        self.Set_Authorization()
      


    #---------------------------------------------------------------------------------------------------------------#
    # Loads credentials from JSON file
    #---------------------------------------------------------------------------------------------------------------#
    def Set_Credentials( self ):
        try:
    
            if ( not os.path.exists( self.CREDENTIALS_FILE ) ):
                raise FileNotFoundError( f"Credentials file '{self.CREDENTIALS_FILE}' not found." )
        
            with open( self.CREDENTIALS_FILE, 'r' ) as f:
                self.Credentials = json.load( f )

            self.Consumer_Key        = self.Credentials["client_id"]
            self.Consumer_Secret     = self.Credentials["client_secret"]
            self.Access_Token        = self.Credentials["Access Token"]
            self.Access_Token_Secret = self.Credentials["Access Secret"]
            self.Bearer_Token        = self.Credentials["bearer_token"]

        except Exception as e:
            self.Logger.Log( f"Encountered an error in Set_Credentials():\n{e}", "Error" )
            return False

    #---------------------------------------------------------------------------------------------------------------#
    # Saves Twitter tweet limit to the credential file
    #---------------------------------------------------------------------------------------------------------------#
    def Save_Credentials( self ):
            
        self.Credentials["API_Tweet_Count"] = self.API_Tweet_Count
        self.Credentials["Date"]            = self.Count_Date
    
        with open( self.CREDENTIALS_FILE, 'w' ) as f:
            json.dump( self.Credentials, f, indent=2 )

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
    # Setup the Authorization based on saved credentials
    #---------------------------------------------------------------------------------------------------------------#
    def Set_Authorization( self ):
        self.Authorization = tweepy.OAuth1UserHandler(
            self.Consumer_Key, 
            self.Consumer_Secret, 
            self.Access_Token, 
            self.Access_Token_Secret
        )

        self.API = tweepy.API( self.Authorization, wait_on_rate_limit=True )

        self.Client = tweepy.Client(
            consumer_key=self.Consumer_Key, 
            consumer_secret=self.Consumer_Secret,
            access_token=self.Access_Token, 
            access_token_secret=self.Access_Token_Secret
        )

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

                # Increasing the social logging for image uploads +1 - not sure if it's required or not
                #self.Rate_Limit.Log_New_Post( "Twitter" )
                return True
            
            else:
                self.Logger.Log( f"Exceeded rate limit, not posing.", "Error" )
                return False

        except Exception as e:
            self.Logger.Log( f"Encountered an error in Add_Media():\n{e}", "Error" )
            return False
        

#---------------------------------------------------------------------------------------------------------------#
# Main start
#---------------------------------------------------------------------------------------------------------------#
if __name__ == '__main__':
    Posting = Post_Content()

    #Posting.Add_Media( r"d:\Data\Pics\temp\IMG_8524.PNG" )
    
    #Posting.Add_Media( r"d:\Data\Pics\temp\IMG_6791.MOV" )

    for i in range( 1, 2 ):
        Current_Time = datetime.now().strftime("%H:%M:%S")
        Text = f"API Testing - {Current_Time}"
        print( Text )
        Test = Posting.Post( f"API Testing - {Text}" )
        time.sleep( 3 )
        if ( Test ):
            Posting.Client.delete_tweet( Test )

    