

#---------------------------------------------------------------------------------------------------------------#
# Load Modules
# py -m pip install --upgrade package_name
#---------------------------------------------------------------------------------------------------------------#
import json
import os
from datetime import datetime, timedelta

#---------------------------------------------------------------------------------------------------------------#
# Class: SocialPostLogger
# Manages logging of social media posts, ensuring that the number of posts within a rolling 24-hour period
# does not exceed the specified daily limit for each social media site.
#---------------------------------------------------------------------------------------------------------------#
class Social_Post_Logger():
    Log_File = None
    Default_Log_Structure = {}
    

    #---------------------------------------------------------------------------------------------------------------#
    # Initializes the SocialPostLogger with the path to the log file and sets up the default structure for each site.
    #---------------------------------------------------------------------------------------------------------------#
    def __init__( self, Log_File=r'data\Dictionaries\Social_Post_Log.json' ):
        self.Log_File = Log_File
        self.Default_Log_Structure = {
            "Twitter": { "Daily Limit": 50, "Posts": [] },
            "Bluesky": { "Daily Limit": 11666, "Posts": [] },
            "Threads": { "Daily Limit": 1, "Posts": [] }
        }

    #---------------------------------------------------------------------------------------------------------------#
    # Reads the log file and returns the log data for the specified social media site.
    # Returns a default structure if the file or the site data does not exist.
    #---------------------------------------------------------------------------------------------------------------#
    def Read_Post_Log( self, site ):
        try:
            if os.path.exists( self.Log_File ):
                with open( self.Log_File, 'r', encoding='utf-8' ) as file:
                    Data = json.load( file )
                    return Data.get( site, { "Daily Limit": 0, "Posts": []} )
            else:
                print( f"Social Log data not found, generating Default Structure for {site}.  Be sure to update the Daily Limit" )
                return self.Default_Log_Structure.get( site, {"Daily Limit": 1, "Posts": []} )
        except Exception as e:
            print( f"Error in Write_Post_Log():\n\t{e}" )
        
    #---------------------------------------------------------------------------------------------------------------#
    # Writes the updated log data for the specified social media site back to the log file.
    #---------------------------------------------------------------------------------------------------------------#
    def Write_Post_Log( self, site, Site_Data ):
        try:
            if os.path.exists( self.Log_File ):
                with open( self.Log_File, 'r', encoding='utf-8' ) as file:
                    Data = json.load( file )
            else:
                Data = {}
            
            Data[site] = Site_Data

            with open( self.Log_File, 'w', encoding='utf-8' ) as file:
                json.dump( Data, file, indent=4 )

        except Exception as e:
            print( f"Error in Write_Post_Log():\n\t{e}" )
    #---------------------------------------------------------------------------------------------------------------#
    # Removes log entries older than 24 hours for the specified social media site.
    #---------------------------------------------------------------------------------------------------------------#
    def Remove_Old_Entries( self, site ):
        try:
            Site_Data = self.Read_Post_Log( site )
            Current_Time = datetime.now()
            Site_Data[ "Posts" ] = [
                Post for Post in Site_Data[ "Posts" ]
                if datetime.fromisoformat( Post ) > Current_Time - timedelta(hours=24)
            ]
            self.Write_Post_Log( site, Site_Data )

        except Exception as e:
            print( f"Error in Count_Recent_Posts():\n\t{e}" )
    #---------------------------------------------------------------------------------------------------------------#
    # Returns the count of posts made in the last 24 hours for the specified social media site.
    #---------------------------------------------------------------------------------------------------------------#
    def Count_Recent_Posts( self, site ):
        try:
            self.Remove_Old_Entries( site )
            Site_Data = self.Read_Post_Log( site )
            return len( Site_Data["Posts"] )
        
        except Exception as e:
            print( f"Error in Count_Recent_Posts():\n\t{e}" )

    #---------------------------------------------------------------------------------------------------------------#
    # Logs a new post by appending the current timestamp to the log for the specified social media site.
    #---------------------------------------------------------------------------------------------------------------#
    def Log_New_Post( self, site ):
        try:
            Site_Data = self.Read_Post_Log( site )
            Current_Time = datetime.now().isoformat()
            Site_Data[ "Posts" ].append( Current_Time )
            self.Write_Post_Log(site, Site_Data)

        except Exception as e:
            print( f"Error in Log_New_Post():\n\t{e}" )

    #---------------------------------------------------------------------------------------------------------------#
    # Checks if posting to the specified social media site is allowed based on the daily limit.
    #---------------------------------------------------------------------------------------------------------------#
    def Can_Post_To_Social_Site( self, site ):
        try:
            Site_Data = self.Read_Post_Log( site )
            if ( self.Count_Recent_Posts( site ) < Site_Data[ "Daily Limit" ] ):
                return True
            else:
                print( f"Post limit reached for {site}. Try again later." )
                return False
        except Exception as e:
            print( f"Error in Can_Post_To_Social_Site():\n\t{e}" )

if __name__ == "__main__":


    # Example usage
    Logger = Social_Post_Logger()()

    print( f"\nTwitter\n")
    if Logger.Can_Post_To_Social_Site( "Twitter" ):
        # Post to Twitter here, and if successful:
        Logger.Log_New_Post( "Twitter" )

    print( f"\nBluesky\n")
    if Logger.Can_Post_To_Social_Site( "Bluesky" ):
        # Post to Bluesky here, and if successful:
        Logger.Log_New_Post( "Bluesky" )

    print( f"\nThreads\n")
    if Logger.Can_Post_To_Social_Site( "Threads" ):
        # Post to Threads here, and if successful:
        Logger.Log_New_Post( "Threads" )

    print()
    print()
    print( f"Twitter posts in the last 24 hours: {Logger.Count_Recent_Posts('Twitter')}" )
    print( f"Bluesky posts in the last 24 hours: {Logger.Count_Recent_Posts('Bluesky')}" )
    print( f"Threads posts in the last 24 hours: {Logger.Count_Recent_Posts('Threads')}" )
