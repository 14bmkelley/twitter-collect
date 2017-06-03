
var fs = require('fs');
var retext = require('retext');
var sentiment = require('retext-sentiment');

var id;
var text;

var retext = retext().use(sentiment).use(function() {
   return function(tree) {
      fs.appendFileSync('aggregate-retext.tsv', id + "\t" + text + "\t"
         + tree.data.polarity + "\n");
   }
});

if (!fs.readdirSync('.').some(file => file === 'aggregate.tsv')) {
   process.exit();
}

var linereader = require('readline').createInterface({
   "input": fs.createReadStream('aggregate.tsv')
});

fs.writeFileSync('aggregate-retext.tsv', '');

linereader.on('line', function(line) {

   var fields = line.split('\t');
   
   id = fields[0];
   text = fields[1].split('\n')[0];
   retext.processSync(text);

});

