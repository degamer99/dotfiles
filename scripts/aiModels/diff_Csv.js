//npm install csv-parser fs
const fs = require('fs');
const csv = require('csv-parser');

const words1 = new Set();
const words2 = new Set();

// Function to load CSV words into a Set
function loadWords(filePath, wordSet, callback) {
  fs.createReadStream(filePath)
    .pipe(csv())
    .on('data', (row) => {
      if (row.word) {
        wordSet.add(row.word.trim());
      }
    })
    .on('end', () => {
      console.log(`Finished reading ${filePath}`);
      callback();
    });
}

// Load both CSVs, then compute the difference
loadWords('first.csv', words1, () => {
  loadWords('second.csv', words2, () => {
    // Compute difference: words in words1 not in words2
    const difference = [...words1].filter(word => !words2.has(word));

    // Write to a new CSV file
    const output = difference.map(word => ({ word }));
    const csvHeader = 'word\n';
    const csvContent = output.map(obj => obj.word).join('\n');

    fs.writeFile('difference.csv', csvHeader + csvContent, (err) => {
      if (err) {
        console.error('Error writing CSV:', err);
      } else {
        console.log('difference.csv has been created with', difference.length, 'words.');
      }
    });
  });
});

