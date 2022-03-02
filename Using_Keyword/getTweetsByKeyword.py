# This code will take a keyword and return the recent tweets, retweets, 
# or mentions that contain the keyword. It will also return information about 
# the user and the location of the tweet and location of the user 
# By: Samer Al-khateeb

# Dependencies: You need to install the requests module
# here is how to do it: Open terminal or CMD:
# For Mac OS users type:
#   python3 -m pip install requests
# For Windows users type:
#   py -m pip install requests
# once you install requests, go to IDLE and run this script

# How to use this script:
# this file can collect data for one keyword or hashtag at a time
# after running the code, you should see an output file called output.csv 

# Do not forget to paste your Bearer Token in the connect_to_twitter() function
# Do not forget to change your keyword in the make_request(headers, nextTokenValue) function
# Do not forget to change the number_of_requests_needed in the main() function

# This is a modified version of the code published here
# https://towardsdatascience.com/getting-started-with-data-collection-using-twitter-api-v2-in-less-than-an-hour-600fbd5b5558

# For the URL paramaters documentation check this 
# https://www.postman.com/twitter/workspace/twitter-s-public-workspace/request/9956214-acd41db7-05bc-4359-be63-dd5249dfef32
import requests
import os
import json
import csv
import time


def connect_to_twitter():
    # Paste your Bearer Token Below
    bearer_token = 'PasteYourBearerTokenHere!'
    return {"Authorization": "Bearer {}".format(bearer_token)}


def make_request(headers, nextTokenValue):    
    #url = "https://api.twitter.com/2/tweets/search/all"
    url = "https://api.twitter.com/2/tweets/search/recent"

    # Paste your keyword or hashtag Below
    keywordORhashtag = '#PutYourHashTagHere!'
    query_params = {
                    'query': '{}'.format(keywordORhashtag),
                    #'start_time': '2022-02-05T07:20:50Z',     # uncomment these if you want to collect
                    #'end_time': '2022-02-08T07:20:50Z',       # data between a specific date and time
                    'max_results': 10,                         # for maximum result returned in a request keeping it at 10 is the best
                    'next_token': nextTokenValue,
                    'expansions': 'author_id,geo.place_id',
                    'tweet.fields': 'id,text,geo,conversation_id,created_at,entities',
                    'place.fields': 'full_name,country',
                    'user.fields':'name,username,location,created_at,description,verified,public_metrics',
                    }
    return requests.request("GET", url, params=query_params, headers=headers).json()


def combine_two_lists(list1, list2):
    # creating a list to hold the output of both lists, i.e., the tweets and the users list
    CSV_output_list = []
    for i in range(len(list1)):
        for j in range(len(list2)):
            if i == j:
                CSV_output_list.append(list1[i] + list2[j])

    return CSV_output_list


def write_output_to_CSV(biglist):
    # creating a file to save the output
    with open('output.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
        #creating a csv writer object 
        csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
        #write the columns headers
        csvwriter.writerow(["USER_ID", "TEXT", "RELATIONSHIP_TYPE", "TEXT_DATE", "TEXT_TIME", "ENTITIES", "USER_DESCRIPTION", "NUMBER_OF_TWEETS", "USER_LOCATION", "USER_NAME", "USERNAME", "NUMBER_OF_FOLLOWERS", "NUMBER_OF_FRIENDS", "NUMBER_OF_LISTS", "USER_VERIFICATION"])
        #writing/inserting the list to the output file 
        csvwriter.writerows(biglist)
    # close the output file
    csv_output_file.close()


def main():

    # Set the number of requests you want to make
    # the maximum allowed is 900 requests per 15 minutes (or 900 seconds) 
    number_of_requests_needed = 900

    # variable to keep count of how many requests made as the loop progress
    number_of_requests = 0

    # the initial value of the nextTokenValue is nothing but it 
    # will be updated in the loop if there are pages of results 
    nextTokenValue = {}

    headers = connect_to_twitter()
    json_response = make_request(headers, nextTokenValue)
    print(json.dumps(json_response, indent=4, sort_keys=True))
    
    #creating a lists to hold the output values related to tweets so we can write it to CSV file
    CSV_output_list_tweets =[]
    # Creating a lists to hold the output values related to users so we can write it to CSV file
    CSV_output_list_users = []

    while (number_of_requests <= number_of_requests_needed):
        # increment the number of requests made
        number_of_requests = number_of_requests + 1
 
        # extract the Tweets info
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

            TEXT_DATE_AND_TIME = json_response['data'][record]['created_at']
            #taking the DATE_AND_TIME column and splitting it into DATE and TIME
            TEXT_DATE_AND_TIME = TEXT_DATE_AND_TIME.split("T")
            TEXT_DATE = TEXT_DATE_AND_TIME[0].strip()
            TEXT_TIME = TEXT_DATE_AND_TIME[1].strip()
        
            #not all tweets has entites defined, if so we assign it undefined value 
            try:
                ENTITIES = json_response['data'][record]['entities']
                #creating a list of values (a row) 
                CSV_output_row = [USER_ID, TEXT, RELATIONSHIP_TYPE, TEXT_DATE, TEXT_TIME, ENTITIES]
                #adding the row to the list of output
                CSV_output_list_tweets.append(CSV_output_row) 
            except KeyError as e:
                #creating a list of values (a row) 
                CSV_output_row = [USER_ID, TEXT, RELATIONSHIP_TYPE, TEXT_DATE, TEXT_TIME, "No Entities"]
                #adding the row to the list of output
                CSV_output_list_tweets.append(CSV_output_row) 
                continue

        # Extract the users Info
        for record in range(len(json_response['includes']['users'])):
            USER_DESCRIPTION = json_response['includes']['users'][record]['description']
            USER_NAME = json_response['includes']['users'][record]['name']
            USERNAME = json_response['includes']['users'][record]['username']
            USER_VERIFICATION = json_response['includes']['users'][record]['verified']

            NUMBER_OF_FOLLOWERS = json_response['includes']['users'][record]['public_metrics']['followers_count']
            NUMBER_OF_FRIENDS = json_response['includes']['users'][record]['public_metrics']['following_count']
            NUMBER_OF_LISTS = json_response['includes']['users'][record]['public_metrics']['listed_count']
            NUMBER_OF_TWEETS = json_response['includes']['users'][record]['public_metrics']['tweet_count']
        
            # NOT all users share their locaiton, if so we assign it undefined value
            try:
                USER_LOCATION = json_response['includes']['users'][record]['location']
                #creating a list of values (a row) 
                CSV_output_row = [USER_DESCRIPTION, NUMBER_OF_TWEETS, USER_LOCATION, USER_NAME, USERNAME, NUMBER_OF_FOLLOWERS, NUMBER_OF_FRIENDS, NUMBER_OF_LISTS, USER_VERIFICATION]
                #adding the row to the list of output
                CSV_output_list_users.append(CSV_output_row) 
            except KeyError as e:
                CSV_output_row = [USER_DESCRIPTION, NUMBER_OF_TWEETS, "Undefined", USER_NAME, USERNAME, NUMBER_OF_FOLLOWERS, NUMBER_OF_FRIENDS, NUMBER_OF_LISTS, USER_VERIFICATION]
                #adding the row to the list of output
                CSV_output_list_users.append(CSV_output_row) 
                continue
        
        # if there are more results match make another request to get it
        if ('next_token' in json_response['meta']):
            # get the next token for next request
            nextTokenValue = json_response['meta']['next_token']
            # make a request using the nextTokenValue to get the rest of the results
            json_response = make_request(headers, nextTokenValue)
            
            print(nextTokenValue)
            print(json.dumps(json_response, indent=4, sort_keys=True))
        else:
            break
        
        # sleep for 1 second so you so not exceed 
        # the 900 requests per 15 minutes limit
        time.sleep(1)

    # send the two lists to the function so we get one list that has all the info
    CSV_output_list = combine_two_lists(CSV_output_list_tweets, CSV_output_list_users)
    
    # write the CSV_output_list to the CSV file
    write_output_to_CSV(CSV_output_list)

 
if __name__ == "__main__":
    main()