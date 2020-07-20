import tweepy
import globalVars

CONSUMER_KEY = globalVars.CONSUMER_KEY
CONSUMER_SECRET = globalVars.CONSUMER_SECRET

def accessTokenGenerator(auth):
	try:
	    redirect_url = auth.get_authorization_url()
	except tweepy.TweepError:
	    print('Error! Failed to get request token.')

	request_token = auth.request_token['oauth_token']

	print(redirect_url)
	# Example using callback (web app)
	# verifier = request.GET.get('oauth_verifier')
	verifier = input('Verifier:')
	# Let's say this is a web app, so we need to re-build the auth handler
	# first...
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	token = request_token

	auth.request_token = { 'oauth_token' : token,
	                         'oauth_token_secret' : verifier }

	try:
	    auth.get_access_token(verifier)
	except tweepy.TweepError:
	    print('Error! Failed to get access token.')

	access_token = auth.access_token
	access_token_secret = auth.access_token_secret

	print("access token", auth.access_token)
	print("access token secret", auth.access_token_secret)

def authorize(auth):
	# Add your API key here
	f = open("tokens.txt", "r")
	access_token, access_token_secret = [line.strip() for line in f]
	auth.set_access_token(access_token, access_token_secret)
	f.close()
	return auth