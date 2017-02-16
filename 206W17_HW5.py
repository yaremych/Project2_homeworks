import unittest
import tweepy
import requests
import json

## SI 206 - W17 - HW5
## COMMENT WITH:
## Your section day/time: Thursdays 3pm
## Any names of people you worked with on this assignment: None

######## 500 points total ########

## Write code that uses the tweepy library to search for tweets with a phrase of the user's choice (should use the Python input function), and prints out the Tweet text and the created_at value (note that this will be in GMT time) of the first THREE tweets with at least 1 blank line in between each of them, e.g.

## TEXT: I'm an awesome Python programmer.
## CREATED AT: Sat Feb 11 04:28:19 +0000 2017

## TEXT: Go blue!
## CREATED AT: Sun Feb 12 12::35:19 +0000 2017

## .. plus one more.

## You should cache all of the data from this exercise in a file, and submit the cache file along with your assignment. 

## So, for example, if you submit your assignment files, and you have already searched for tweets about "rock climbing", when we run your code, the code should use CACHED data, and should not need to make any new request to the Twitter API. 
## But if, for instance, you have never searched for "bicycles" before you submitted your final files, then if we enter "bicycles" when we run your code, it _should_ make a request to the Twitter API.

## The lecture notes and exercises from this week will be very helpful for this. 
## Because it is dependent on user input, there are no unit tests for this -- we will run your assignments in a batch to grade them!

## We've provided some starter code below, like what is in the class tweepy examples.

## **** For 50 points of extra credit, create another file called twitter_info.py that contains your consumer_key, consumer_secret, access_token, and access_token_secret, import that file here, and use the process we discuss in class to make that information secure! Do NOT add and commit that file to a public GitHub repository.

## **** If you choose not to do that, we strongly advise using authentication information for an 'extra' Twitter account you make just for this class, and not your personal account, because it's not ideal to share your authentication information for a real account that you use frequently.

## Get your secret values to authenticate to Twitter. You may replace each of these with variables rather than filling in the empty strings if you choose to do the secure way for 50 EC points
consumer_key = "ovCRJvM7TRA6lRGsVw9k9wCId"
consumer_secret = "4n6TeEHWolf8d5Uzm8opWjaDHh7ryloATtGnuMWxyhSY82CCPK"
access_token = "252819439-GLwVeEdXM8m9Wp16jlqSIltwJk57ygNR5rLsvq7e"
access_token_secret = "A18dGpNGKyXQLsos43HvgGz6EJqqsYFxczzt2gVlrYc4i"
## Set up your authentication to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser()) # Set up library to grab stuff from twitter with your authentication, and return it in a JSON-formatted way

## Write the rest of your code here!

#### Recommended order of tasks: ####
## 1. Set up the caching pattern start -- the dictionary and the try/except statement shown in class.
## 2. Write a function to get twitter data that works with the caching pattern, so it either gets new data or caches data, depending upon what the input to search for is. You can model this off the class exercise from Tuesday.
## 3. Invoke your function, save the return value in a variable, and explore the data you got back!
## 4. With what you learn from the data -- e.g. how exactly to find the text of each tweet in the big nested structure -- write code to print out content from 3 tweets, as shown above.


## First set up the caching 
CACHE_FNAME = "twitter_cache.json"
try:
	cache_file_obj = open(CACHE_FNAME,'r')
	cache_contents = cache_file_obj.read()
	CACHE_DICTION = json.loads(cache_contents)
except:
	CACHE_DICTION = {}
	# I know that in my code 
	# Inside a function that gets data from the internet
	# I will have to make sure that I properly add data to cache_diction
	# I will have to make sure that I properly write CACHE_DICTION to a file, so I'll have it next time I run my program


## Function to make sure that params always end up in the same order inside the URL
def canonical_order(d):
    alphabetized_keys = sorted(d.keys())
    res = []
    for k in alphabetized_keys:
        res.append((k, d[k]))
    return res


## This is the function that actually builds each URL to make a request with, so we can say "Have we made a request with this URL before?" It invokes the  canonical_order function in the process. For requests where we can access the URL, this is a good unique identifier.
def requestURL(baseurl, params = {}):
    req = requests.Request(method = 'GET', url = baseurl, params = canonical_order(params))
    prepped = req.prepare()
    return prepped.url


## Now create a function similar to meaning_relation_caching in the datamuse example --- set up the request, and check if we've made a request with that specific URL before (ie: the exact same params and exact same things passed into the params). If we have, just use the cached data. If not, make a new request and cache that data! 

## Let's figure out how to make the necessary request to twitter first: 

# search tweets based on text input from the user
# return text and created_at
# for the first 3 tweets

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

phrase = input("Enter a word or phrase you'd like to see tweets about: ")

results = api.search(q=phrase)

#print(type(results)) # it is a dictionary
#print(results.keys()) # keys are 'statuses' and 'search_metadata' (we are probably just interested in the statuses part)
#print(results['statuses'][0].keys())

# results['statuses'] gets us to a list; each element in the list represents one tweet, and is a dictionary
# each tweet dictionary has various keys that hold info about it. we want: ['text'] and ['created_at']

print(results['statuses'][0]['text'])
print(results['statuses'][0]['created_at'])

# WOOO!
# now print out that info for the first 3 tweets

for x in range(3):
	print("\n")
	print("TEXT: " + results['statuses'][x]['text'])
	print("CREATED AT: " + results['statuses'][x]['created_at'])
print("\n")

## Now write code so that we can use cached data if possible: 

def twitter_search_caching(phrase):
	# still need the basics to make a request -- in case!

	#api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

	# but have to determine what makes this request unique
	# requestURL takes base url and params dict and composes the URL -- will always be the same with the same info
	unique_identifier = requestURL(base_url,params_diction)
	## then -- have we seen this unique identifier before in our cache?
	if unique_identifier in CACHE_DICTION:
		print("using cached data for", unique_identifier)
		# cool, if so, grab the data that goes with it!
		python_obj_data = CACHE_DICTION[unique_identifier]
	else: # if not
		print("getting new data from the web for", unique_identifier)
		# get data from the internet
		response = requests.get(base_url,params=params_diction)
		python_obj_data = json.loads(response.text) # the JSON-formatted string loaded into a python dictionary
		# but also! cache the data, so next time we won't have to make a request to the internet, get the same stuff
		# so,
		CACHE_DICTION[unique_identifier] = python_obj_data
		f = open(CACHE_FNAME,'w') # open our cache file to write
		f.write(json.dumps(CACHE_DICTION)) # write the JSON-string version of the cache dictionary to the file, which has everything in it
		f.close() # close up the file for now
	# now no matter what we got the python object we want in the variable python_obj_data, so let's go ahead w/ what we were doing
	final_list = []
	for word_diction in python_obj_data[:3]:
		final_list.append(word_diction["word"])
	return final_list






