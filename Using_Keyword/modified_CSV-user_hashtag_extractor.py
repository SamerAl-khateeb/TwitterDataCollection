# A code to extract User X Hashtag network   By: Samer Al-khateeb
#################################################################
#this is a modified version of the CSV-user_hashtag_extractor.py
#so it can work with the data collected from getTweetsByKeyword.py

#rename the output.csv file you obtained from running getTweetsByKeyword.py
#into input.csv and save it in the same directory as this code
#remove the header of the file (the first row in the file)
#run this code and you should see User-Hashtag-Network.csv generated 

import csv

def main():
  #counter to keep track of the rows processed
  count = 0
  
  #creating a list to hold the output values so we can write it to CSV file
  CSV_output_list =[]

  #variable that hold the file name
  input_filename = 'input.csv'

  #open the input file and read it
  with open(input_filename, newline='', encoding='utf-8') as csv_input_file:
    CSV_file_as_list = csv.reader(csv_input_file, skipinitialspace=True)
    
    #process each ron in the input file
    for row in CSV_file_as_list:
      count = count +1
      print()
      print("Processing row#", count)
      print()
    
      id_str = row[0]                            #--> kept it as is
      from_user = row[10]                        #--> changed it to row[10]
      text = row[1]                              #--> changed it to row[1]   


      #to determin the type of the relationship
      #if(text[0] == 'R' and text[1] == 'T'):    #--> commented out
       # relationship_type = 'retweet'           #--> commented out
      #elif (text.find('@') != -1):              #--> commented out
       # relationship_type = 'mention'           #--> commented out
      #else:
       # relationship_type = 'tweet'             #--> commented out
      
      relationship_type = row[2]                 #--> added this line of code

      #taking the time column and splitting it into date and time
      #relation_date_and_time = row[4].split(" ")                   #--> commented out
      #relation_date = relation_date_and_time[0].strip()            #--> commented out
      #relation_time = relation_date_and_time[1].strip()            #--> commented out

      relation_date = row[3]             #--> added this line of code
      relation_time = row[4]             #--> added this line of code

      user_followers_count = row[11]       #--> changed it to row[11]  
      user_friends_count = row[12]         #--> changed it to row[12] 
      user_location = row[8]              #--> changed it to row[8] 
      entities_str = row[5]              #--> changed it to row[14] 
      

      #added the other columns in the row
      user_description = row[6]            #--> added this line of code
      number_of_tweets = row[7]            #--> added this line of code
      number_of_lists = row[13]            #--> added this line of code
      user_verification = row[14]          #--> added this line of code
      name = row[9]                        #--> added this line of code
      


      #removing quotes from entities_str column
      entities_Str_NoQuotes = entities_str.strip('"')

      #converting the string to Dictionary
      jsonColumnData = eval(entities_Str_NoQuotes)

      #each User Mentioned in the jsonColumnData is 
      #nested inside the jsonColumnData["urls"]
      if "hashtags" in jsonColumnData:                      #--> added this if statement
        for eachHashtag in jsonColumnData["hashtags"]:
          #creating a file to save the output
          with open('User-Hashtag-Network.csv', 'w', newline='', encoding='utf-8') as csv_output_file:
            #creating a csv writer object 
            csvwriter = csv.writer(csv_output_file, delimiter=',', lineterminator='\n')
          
            #write the columns headers
            csvwriter.writerow(["source", "name", "text", "relationship_type", 
              "relation_date", "relation_time", "user_followers_count", 
              "user_friends_count", "number_of_tweets", "number_of_lists", 
              "user_description", "user_verification","hashtag"])                  #--> updated this line of code
          
            #creating a list of values (a row) 
            CSV_output_row = [from_user, name, text, relationship_type, 
              relation_date, relation_time, user_followers_count, 
              user_friends_count, number_of_tweets, number_of_lists,
              user_description, user_verification, eachHashtag["tag"]]              #--> updated this line of code
          
            #adding the row to the list of output
            CSV_output_list.append(CSV_output_row) 
          
            #writing/inserting the list to the output file 
            csvwriter.writerows(CSV_output_list)

          csv_output_file.close()
  csv_input_file.close()
main()


