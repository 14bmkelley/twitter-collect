
var fs = require('fs');
var datetime = require('node-datetime');
var TwitterStream = require('twitter');

var now = datetime.create().format('Y.m.d-H.M.S');
var directory = "tweets-batch-" + now;

//fs.mkdirSync(directory);

var client = new TwitterStream({
   "access_token_key": "2392021202-5pL3qI6aXGloucwinyOwEp5XScU9f4LyXihDHA6",
   "access_token_secret": "5j6Wqsx7V6GH7oGhII8XYGXDtmUnrfJe6IkjyCAtoYgdb",
   "consumer_key": "W7DE359Mjc8NJlaR5E6bdBv8d",
   "consumer_secret": "G4SQ5OTR6lyRIthyFIDY2bOgzW8WUGIwrMM6axxGseaPUiI2s9"
});

var stream = client.stream('statuses/sample', {});

var endstream = false;

fs.writeFileSync('streamed-tweets-corpus.json', '{ "streamed_tweets": [');

stream.on('data', function(data) {

   if (endstream) {
      fs.appendFileSync('streamed-tweets-corpus.json', 'null ] }');
      process.exit();
   }

   if (data.lang === 'en') {

      if (data.text.substring(0, 2) === 'RT') {
         data.text = data.text.substring(2, data.text.length);
      }

      fs.appendFileSync('streamed-tweets-corpus.json', JSON.stringify(data) + ',');

      //var filename = directory + "/tweet-" + data.id_str + '.tsv';

      //var contents = data.id_str + "\t"
      //   + data.text.replace(/\s+/g, " ").replace(/[^\x00-\x7F]/g, "") + "\n";

      //fs.writeFile(filename, contents);

   }

});

process.openStdin().addListener("data", function(data) {
   endstream = true;
});

