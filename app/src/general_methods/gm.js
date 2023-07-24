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


function sleep(sec) {
    return new Promise(resolve => setTimeout(resolve, sec * 1000));
}


function fetchFlag(flagName, defaultValue = false) {
    for (const element of process.argv) {
        if (element == flagName) {
            return !defaultValue;
        }
    }
    return defaultValue;    
}


function getArg(argName) {
    let args = [];
    process.argv.forEach(function (val, index, array) {
        args.push([index, val])
    });

    let argVal = null;
    for (const arg of args) {
        if (arg[1] == argName) {

            if (args[arg[0] + 1]) {
                argVal = args[arg[0] + 1][1];
                break
            }
        }
    }

    if (argVal === null) {
        console.log('Required ' + argName);
        process.exit(1)
    }
    else {
        return argVal;
    }
}


function help(message) {
    if (fetchFlag("--help") || fetchFlag("-h")) {
        console.log(message);
        process.exit();
    } 
}


module.exports = {
   sleep,
   writeFile,
   readFile,
   getArg,
   fetchFlag,
   help,
}