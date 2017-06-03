
var fs = require('fs');
var analyze = require('sentiword');
var request = require('request');
var unfluff = require('unfluff');

if (!fs.readdirSync('.').some(file => file === 'aggregate.tsv')) {
   process.exit();
}

var linereader = require('readline').createInterface({
   "input": fs.createReadStream('aggregate.tsv')
});

fs.writeFileSync('aggregate-sentiword.tsv', '');

request('https://www.npmjs.com/package/request', function(error, response, body) {
   if (!error) {
      var ranking = analyze(unfluff(body).text);
   }
});

linereader.on('line', function(line) {

   var fields = line.split('\t');
   
   var id = fields[0];
   var text = fields[1].split('\n')[0];
   var urlRegex = /https{0,1}:[^\s]+/g;
   var urls = text.match(urlRegex);
   var ranking = analyze(text);

   if (urls) {
      sentimentFromUrl(urls[0], function(sentiment) {
         console.log(sentiment);
      });
   }
   
   else {
      writeFile(ranking.sentiment, id + "\t" + text + "\t" + ranking.sentiment + "\n");
   }

});

function sentimentFromUrl(url, callback) {
   console.log(url);
   request(url, function(error, response, body) {
      if (!error) {
         console.log(unfluff(body).text);
         callback(analyze(unfluff(body).text).sentiment);
      }
   });
}

function writeFile(sentiment, text) {
   
   if (sentiment > -0.6) {
      return;
   }

   fs.appendFileSync('aggregate-sentiword.tsv', text);

}

