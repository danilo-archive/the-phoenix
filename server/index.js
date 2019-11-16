const express = require('express')
const fs = require('fs');
const app = express()
const port = 3000

app.get('/', (req, res) => res.sendFile(__dirname + '/public/index.html'))
app.use(express.static('public'))
app.listen(port, () => console.log(`Listening on :${port}!`))

fs.readFile("station_codes.csv", "utf8",function (err, data) {
    if (err) throw err;
    const dataString = processCsvData(data)
});

const processCsvData = function(data){

    var output = []
    var nameKey = "name";
    var crsKey = "crs";

    var array  = data.split("\n");
    
    array.forEach(element => {
        output.push(
            {
                nameKey : element.split(',')
            }
        )
    });
}