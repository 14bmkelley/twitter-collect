
var fs = require('fs');
var analyze = require('Sentimental').analyze;

if (!fs.readdirSync('.').some(file => file === 'aggregate.tsv')) {
   process.exit();
}

var linereader = require('readline').createInterface({
   "input": fs.createReadStream('aggregate.tsv')
});

fs.writeFileSync('aggregate-sentimental.tsv', '');

linereader.on('line', function(line) {

   var fields = line.split('\t');
   
   var id = fields[0];
   var text = fields[1].split('\n')[0];
   var ranking = analyze(text);

   fs.appendFileSync('aggregate-sentimental.tsv', id + "\t" + text + "\t" + ranking.score + "\n");

});

