
var fs = require('fs');
var lda = require('lda');

if (!fs.readdirSync('.').some(file => file === 'aggregate-sentiword.tsv')) {
   process.exit();
}

var linereader = require('readline').createInterface({
   "input": fs.createReadStream('aggregate-sentiword.tsv')
});

var documents = [];

linereader.on('line', function(line) {

   var fields = line.split('\t');
   
   var id = fields[0];
   var text = fields[1];

   documents.push(text);

});

linereader.on('close', function() {

   console.log(lda(documents, 50, 1));

});

