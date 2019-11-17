const fs = require('fs')
let datapack =     JSON.parse(fs.readFileSync('pretty_data.json'));



console.log(datapack)