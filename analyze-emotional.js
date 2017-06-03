
var fs = require('fs');
var emotional = require('emotional');

emotional.load(function() {

   if (!fs.readdirSync('.').some(file => file === 'aggregate.tsv')) {
      process.exit();
   }

   var linereader = require('readline').createInterface({
      "input": fs.createReadStream('aggregate.tsv')
   });

   fs.writeFileSync('aggregate-emotional.tsv', '');

   linereader.on('line', function(line) {

      var fields = line.split('\t');
   
      var id = fields[0];
      var text = fields[1].split('\n')[0];
      var ranking = emotional.get(text);

      fs.appendFileSync('aggregate-emotional.tsv',
            id + "\t" + text + "\t" + ranking.polarity + "\t"
            + ranking.subjectivity + "\n");

   });

});

