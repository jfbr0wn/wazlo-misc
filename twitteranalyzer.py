import sys
import requests
import json
import twitter
import config

# this function grabs the relevant data for the json file
def convert_status_to_pi_content_item(s):
    return {
        'id': str(s.id),
        'contenttype': 'text/plain',
        'language': s.lang,
        'content': s.text,
        'created': s.created_at_in_seconds,
    }


#handle = sys.argv[1]

# twitter handle of user
handle = 'realDonaldTrump'

# sets up the twitter api with all the correct keys from the config file
twitter_api = twitter.Api(consumer_key=config.twitter_consumer_key,
                          consumer_secret=config.twitter_consumer_secret,
                          access_token_key=config.twitter_access_token,
                          access_token_secret=config.twitter_access_secret,
                          debugHTTP=True)

max_id = None
statuses = []

# pulls 16 lots of tweets (200 per lot for total 3200 tweets)
for x in range(0, 16):  # Pulls max number of tweets from an account
    if x == 0:
        statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                       count=200,
                                                       include_rts=False)
        status_count = len(statuses_portion)
        max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
    else:
        statuses_portion = twitter_api.GetUserTimeline(screen_name=handle,
                                                       count=200,
                                                       max_id=max_id,
                                                       include_rts=False)
        if statuses_portion == []:
            break
        
        status_count = len(statuses_portion)
        max_id = statuses_portion[status_count - 1].id - 1  # get id of last tweet and bump below for next tweet set
    
    # makes a giant variable with all the statuses
    for status in statuses_portion:
        statuses.append(status)

# runs the statuses through the function, making an array
pi_content_items_array = list(map(convert_status_to_pi_content_item, statuses))

# if its the firt time running code
check=0

# for all the tweets, make a list
for c in range(0, len(pi_content_items_array)):
    if pi_content_items_array[c]['language'] in ['en', 'es', 'ja', 'ar', 'ko']:
        if check == 0:
            new_list = [pi_content_items_array[c]]
            check = 1
        else:
            new_list.append(pi_content_items_array[c])

# add the start of the dict
pi_content_items = {'contentItems': new_list}

# saves data to the json
with open('twitter.json', 'w') as outfile:
    json.dump(pi_content_items, outfile, sort_keys=True, indent=4)

# end of code