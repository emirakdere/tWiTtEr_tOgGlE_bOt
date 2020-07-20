import authBot
import string
import re
import time
import sys
import tweepy

# local globalVars.py, which contains:
# 	BEARER = auth 2 bearer token given when you sign up for your developer account 
# 	CONSUMER_KEY = 
# 	CONSUMER_SECRET = 
# 	CELEB_USER_NAMES = 
import globalVars

# TODO:
#		strip mentions

CONSUMER_KEY = globalVars.CONSUMER_KEY
CONSUMER_SECRET = globalVars.CONSUMER_SECRET

f2 = open("tweetsLog.txt", "w")
AUTH = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
AUTH = authBot.authorize(AUTH)
API = tweepy.API(AUTH)
CELEB_USER_IDS = []


def removePattern(pattern, text):
	newText = []
	curPosition = 0
	matches = re.finditer(pattern, text, re.IGNORECASE)
	if matches != None:
		for m in matches:
			newText.append(text[curPosition:m.start()])
			curPosition = m.end()
	newText.append(text[curPosition:len(text)])
	return "".join(newText)

def toggleCase(text):
	text = list(text)
	for i in range(len(text)):

		if text[i] in set(string.ascii_letters):
			#ensure it is capital letter
			text[i] = text[i].upper() if i % 2 == 1  else text[i]

	return "".join(text)

def printTweetInfo(statusObj):
	for field in statusObj._json:
		print(field, "\n", statusObj._json[field], "\n")


for name in globalVars.CELEB_USER_NAMES:
	CELEB_USER_IDS.append(API.get_user(name).id_str)

class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		if (not hasattr(status, "retweeted_status")) and status.lang == "tr" and status.user.id_str in CELEB_USER_IDS:

			status = API.get_status(status.id, tweet_mode="extended")

			text = status.full_text if hasattr(status, "full_text") else status.text
			text = text.lower()
			
			if re.search("(şeh(i|a)(d|t)\S*)|(vef(a|â)(t|d)\S*)|(üzü[l|n]\S*)|(y(â|a)d)|(anıyor\S*)|(ölüm)", text) == None:#, re.IGNORECASE) # don't need it since all incoming str is lowercase
	        	
				text = removePattern("https?:[\S]*", text)
				text = removePattern(" @[\S]")

				# adding the link makes it so that you are "retweeting with comment"
				text = toggleCase(text) + " " + "https://twitter.com/" + status.user.screen_name + "/status/" + status.id_str
				print("@", status.user.screen_name, ": ", text)

				# for replying to the tweet you are trolling, remove the comment
				API.update_status(text) #, in_reply_to_status_id=status.id, auto_populate_reply_metadata=True)
				f2.write(str(status._json))


	def on_error(self, status_code):
		print(status_code, file=sys.stderr)
		if status_code == 420:
            #returning False in on_error disconnects the stream
			return False
        # returning non-False reconnects the stream, with backoff.



if __name__ == "__main__":
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth=API.auth, listener=myStreamListener, tweet_mode="extended")
	myStream.filter(follow=CELEB_USER_IDS, is_async=True)




