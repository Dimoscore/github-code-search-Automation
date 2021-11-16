# Import required modules
import requests
import time
import sys

def banner1():
  print(""" 
  ____ _ _   _   _       _        ____          _      
 / ___(_) |_| | | |_   _| |__    / ___|___   __| | ___
| |  _| | __| |_| | | | | '_ \  | |   / _ \ / _` |/ _ /
| |_| | | |_|  _  | |_| | |_) | | |__| (_) | (_| |  __/
 \____|_|\__|_| |_|\__,_|_.__/   \____\___/ \__,_|\___|

  ____           _     _
 / ___|_ __ __ _| |__ | |__   ___ _ __
| |  _| '__/ _` | '_ \| '_ \ / _ \ '__|
| |_| | | | (_| | |_) | |_) |  __/ |
 \____|_|  \__,_|_.__/|_.__/ \___|_|


# A Simple Tool To Search Github Public Code and Fetch All Results Inside TXT File
# Coded By Amr-Khaled - @Amr9k8


""")  
    
def RequirmentsCheck():
    if mytoken[10] == "x":
        print("You Must Create Github Token First")
        exit()

    if not file:
        print("Please Write the textfile path ,to store resutls in")
        exit()


def get_rate_limit():
    rateLimit = requests.get("https://api.github.com/rate_limit",headers={
        'Authorization':mytoken,
        }).json()
    return(rateLimit['resources'])

def countdown():
    t=10
    rateLimit = get_rate_limit()
    while rateLimit['search']['remaining'] == 0:
        rateLimit = get_rate_limit()
        print("Reached Primary Rate Limit => Sleeping For : "+str(t)+" Seconds", end="\r")
        time.sleep(1)
        t -= 1
        if t == 0:
            t=10
def countdownSecondaryLimit(query,pageNumber):
    t=0
    #response = send_request(query,pageNumber)
    while t < 6:
        print("Reached Secondary Rate Limit => Waiting : "+str(t)+" Seconds", end="\r")
        time.sleep(1)
        t += 1
    print("\n Back To Work ! \n")

def send_request(mytoken,word,pageNumber = 0):
    if pageNumber != 0:
        urlxx ='https://api.github.com/search/code?q='+word+'&page='+str(pageNumber)

    else:
        urlxx ='https://api.github.com/search/code?q='+word
    #print(urlxx)
    response = requests.get(urlxx,headers={
    'Authorization':mytoken,
    'Accept':'application/vnd.github.v3.text-match+json'
    }).json()
    time.sleep(5)
    return response



# To create an access token
# first create account  on github then visit this link to generate token - https://github.com/settings/tokens
# Paste your Access token , Note Replace only the xxxxxxx with key and  keep "token  "
mytoken = 'token xxxxxxxxxxxxxxxxxxxxxxxxx' #example : 'token ghp_dBuJHMxCIxXJimzJgMD1M43D24Cw'
# Full Path to the textfile which will store the resutls 
file  = "results.txt" #example:  "D:\\Users\\Amr\\Desktop\\github uploads\\Github Grabber\\results.txt"


RequirmentsCheck()

open(file, "w").close()
total_pages = 1
banner1()
query = input("\n\nEnter Text To Search ")



# Just test
response = send_request(mytoken,query,3,)

if(len(response) > 2):
    rate_limit = get_rate_limit()
    if (rate_limit['search']['remaining'] != 0):
        response = send_request(mytoken,query)
        if(response['total_count'] >=1000):
            total_count = 1000
            total_pages = 35
        else:
            total_count = response['total_count']
            total_pages = int(total_count/30)+1
        
        print("\nFound [ " + str(total_count)+ "] Results\n")
        print("\nTotal Pages To Fetch Text From : "+str(total_pages-1)+"\n")
    else:
        countdown()
else:
        print(response)
        countdownSecondaryLimit(query,3)  


pageNumber=1
while pageNumber in range(1,total_pages+1):
    response = send_request(mytoken,query,pageNumber)

    if(len(response) > 2):# check if Secondary rate limit off
            rate_limit = get_rate_limit()
            if (rate_limit['search']['remaining'] != 0):  # check if Primary rate limit off 
                print("Grabbin Text From Page["+str(pageNumber)+ "]",end="\r")
                pageNumber+=1  
                for oneitem in response['items']:
                    for one_text in oneitem['text_matches']:
                            objectt = one_text['fragment']
                            with(open(file ,'a',encoding='utf-8') )as textfile:
                                textfile.write(objectt)
            else:
                countdown()
    else:
        print(response)
        countdownSecondaryLimit(query,pageNumber)      
        


print("\n \n"+ "Results Saved Successfully From "+ str(pageNumber-1) + " Pages \n \n ")