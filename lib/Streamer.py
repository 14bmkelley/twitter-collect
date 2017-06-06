
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

class Streamer:

    def __init__(self):
        self.oauth_handler = None
        self.twitter_stream = None

    def set_credentials(self, token, token_secret, key, key_secret):
        self.oauth_handler = OAuthHandler(key, key_secret)
        self.oauth_handler.set_access_token(token, token_secret)

    def set_track(self, track):
        self.track = track

    def set_on_data(self, on_data):
        self.on_data = on_data

    def stream(self, keywords):
        
        listener = self.Listener()
        
        if self.on_data is not None:
            listener.set_on_data(self.on_data)

        self.twitter_stream = Stream(self.oauth_handler, listener)

        if keyword == None:
            self.twitter_stream.sample()
        else:
            self.twitter_stream.filter(track=list(keywords))

    class Listener(StreamListener):

        def set_on_data(self, on_data):
            self.custom_on_data = on_data

        def on_data(self, data):
            self.custom_on_data(data)
            return True

        def on_error(self, error):
            print('error: ' + str(error))

