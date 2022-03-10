# This code will give you the last 10 tweets, retweets, or mentions made by a user
# By: Samer Al-khateeb

# Dependencies: You need to install the requests module
# here is how to do it: Open terminal or CMD:
# For Mac OS users type:
#   python3 -m pip install requests
# For Windows users type:
#   py -m pip install requests
# once you install requests, go to IDLE and run this script

# How to use this script:
# the input_file.txt need to have one username in each line
# after running the code, you should see an output file called output.csv

# Make sure your input file in in the same folder as this script 
# Do not forget to paste your Bearer Token


# this is a modified version of the code published here
# https://github.com/twitterdev/Twitter-API-v2-sample-code/blob/main/User-Tweet-Timeline/user_tweets.py

import requests
import os
import json
import csv


# Paste your Bearer Token Below
bearer_token = 'PasteYourBearerTokenHere!'


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    #print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    # a list that will be used to collect the users IDs
    list_of_user_ids = []

    #creating a list to hold the output values so we can write it to CSV file
    CSV_output_list =[]

    #an input file contain list of usernames
    filename = "input_file.txt"
    #open the file 
    input_file = open(filename, "r")
    #read the content of the file
    input_file_contents = input_file.read()
    #take off the new line charecter from the end of each username
    contents_split = input_file_contents.splitlines()

    # for each username in the file send a request to retrieve it's user ID
    # I got the URL from here
    # https://www.postman.com/twitter/workspace/twitter-s-public-workspace/request/9956214-288337e6-91e5-4297-bde2-cae96a549732
    for user_name in contents_split:
        url = "https://api.twitter.com/2/users/by/username/{}?".format(user_name)
        params = ""
        json_response = connect_to_endpoint(url, params)
        #print(json.dumps(json_response, indent=4, sort_keys=True))
        json_data_returned = json_response['data']['id']
        list_of_user_ids.append(json_data_returned)
    print(list_of_user_ids)
    #close the input file
    input_file.close()    

    # for each user ID collect it's tweets
    # I got the URL from here 
    # https://www.postman.com/twitter/workspace/twitter-s-public-workspace/request/9956214-71515dbc-fb46-4e88-b3f1-5918e3de64a6 
    for user_id in list_of_user_ids:
        url = "https://api.twitter.com/2/users/{}/tweets".format(user_id)
        params = "tweet.fields=author_id,text,created_at,geo,lang,in_reply_to_user_id,referenced_tweets,entities,source"
        json_response = connect_to_endpoint(url, params)
        print(json.dumps(json_response, indent=4, sort_keys=True))
        
        #go through the response received for each user and extract these info
        for record in range(len(json_response['data'])):
            USER_ID = json_response['data'][record]['author_id']
            
            TEXT = json_response['data'][record]['text']
            #to determin the type of the relationship
            if(TEXT[0] == 'R' and TEXT[1] == 'T'):
                RELATIONSHIP_TYPE = 'retweet'
            elif (TEXT.find('@') != -1):
                RELATIONSHIP_TYPE = 'mention'
            else:
                RELATIONSHIP_TYPE = 'tweet'

            DATE_AND_TIME = json_response['data'][record]['created_at']
            #taking the DATE_AND_TIME column and splitting it into DATE and TIME
            DATE_AND_TIME = DATE_AND_TIME.split("T")
            DATE = DATE_AND_TIME[0].strip()
            TIME = DATE_AND_TIME[1].strip()

            TEXT_LANGUAGE = json_response['data'][record]['lang']
            DEVICE_USED = json_response['data'][record]['source']
            
            try:
                ENTITIES = json_response['data'][record]['entities']
                #EXPANDED_URL = json_response['data'][record]['entities']['urls'][0]['expanded_url']
                #HASHTAG = json_response['data'][record]['entities']['hashtags'][0]['tag']
                #USERS_MENTIONED = json_response['data'][record]['entities']['mentions']

                #creating a list of values (a row) 
                CSV_output_row = [USER_ID, TEXT, RELATIONSHIP_TYPE, DATE, TIME, TEXT_LANGUAGE, DEVICE_USED, ENTITIES]
                #adding the row to the list of output
                CSV_output_list.append(CSV_output_row) 
            
            except KeyError as e:
                #creating a list of values (a row) 
                CSV_output_row = [USER_ID, TEXT, RELATIONSHIP_TYPE, DATE, TIME, TEXT_LANGUAGE, DEVICE_USED, "No Entities"]
                #adding the row to the list of output
                CSV_output_list.append(CSV_output_row) 
                continue

        #creating a file to save the output
        with open('output.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
            #creating a csv writer object 
            csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
            #write the columns headers
            csvwriter.writerow(["USER_ID", "TEXT", "RELATIONSHIP_TYPE", "DATE", "TIME", "TEXT_LANGUAGE", "DEVICE_USED", "ENTITIES"])
            #writing/inserting the list to the output file 
            csvwriter.writerows(CSV_output_list)
        # close the output file
        csv_output_file.close()


if __name__ == "__main__":
    main()