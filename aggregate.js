
var fs = require('fs');

var folders = fs.readdirSync('.').filter(file => file.substring(0, 6) === 'tweets');

fs.writeFileSync('aggregate.tsv', '');

for (var folder of folders) {

   var folderFiles = fs.readdirSync(folder);

   fs.writeFileSync(folder + '/aggregate.tsv', '');

   for (var folderFile of folderFiles) {
         
      var contents = fs.readFileSync(folder + '/' + folderFile)
         .toString('utf8').split("\t");

      var id = contents[0];
      var text = contents[1].split("\n")[0];

      if (text.substring(0, 2) === 'RT') {
         text = text.substring(3, text.length);
      }

      var result = id + "\t" + text + "\n";

      fs.appendFileSync(folder + '/aggregate.tsv', result);
      fs.appendFileSync('aggregate.tsv', result);

   }

}

