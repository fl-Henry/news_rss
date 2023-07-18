const fs = require('fs');


function readFile(filePath)
{
    try {
      const data = fs.readFileSync(filePath, 'utf8');
      return data;
    } catch (err) {
      console.error(err);
    }
}


function writeFile(filePath, content)
{
    try {
      fs.writeFileSync(filePath, content);
      // file written successfully
    } catch (err) {
      console.error(err);
    }
}


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


module.exports = {
   sleep,
   writeFile,
   readFile,
}