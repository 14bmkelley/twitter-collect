
var fs = require('fs');
var TwitterCollector = require('twitter-collect');

var corpus = JSON.parse(fs.readFileSync('./streamed-tweets-corpus.json')).streamed_tweets;

var collector = new TwitterCollector({
   
   select: function(tweet_data, callback) {
      
      if (tweet_data && tweet_data.lang && tweet_data.text) {
         var lang = tweet_data.lang === 'en';
         var tag = tweet_data.text.match(/@realDonaldTrump([^\\w]|$)/g);
         var hash = tweet_data.text.match(/#trump([^\\w]|$)/g);
         callback(lang && (tag || hash));
      }
      else {
         callback(false);
      }

   },

   track: 'trump',
   corpus_size: 5000,
   topic_count: 10,
   
   credentials: {
      access_token_key: "2392021202-5pL3qI6aXGloucwinyOwEp5XScU9f4LyXihDHA6",
      access_token_secret: "5j6Wqsx7V6GH7oGhII8XYGXDtmUnrfJe6IkjyCAtoYgdb",
      consumer_key: "W7DE359Mjc8NJlaR5E6bdBv8d",
      consumer_secret: "G4SQ5OTR6lyRIthyFIDY2bOgzW8WUGIwrMM6axxGseaPUiI2s9"
   },

   corpus: corpus

});

collector.collect(null, function(results) {
   console.log(results);  
});

