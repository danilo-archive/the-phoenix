const express = require('express')
const fs = require('fs');
const app = express()
const port = 3000

app.get('/', (req, res) => res.sendFile(__dirname + '/public/index.html'))
app.use(express.static('public'))
app.listen(port, () => console.log(`Listening on :${port}!`))

fs.readFile("station_codes.csv", "utf8",function (err, data) {
    if (err) throw err;
    const processedData = processCsvData(data)
    fs.writeFile("station_codes.json", JSON.stringify(processedData), "utf8", (err)=>console.error(err))
});

const processCsvData = function(data){

    var output = []
    var nameKey = "name";
    var crsKey = "crs";

    var array  = data.split("\n");
    
    array.forEach(element => {
        var a = element.split(',');
        output.push(
            {
                name : a[0].toLowerCase().replace(' ', '').replace(' ', '').replace(' ', '').replace(' ', '') ,  
                crs : crsCode(a[1])
            }
        )
    });

    
    return output;
}

const crsCode = function(c){
    try {
        return c.replace('\r', '')
      }
      catch(error) {
       return c
      }
      
}