const express = require('express')
const fs = require('fs');   
const app = express()
const port = 3000

app.get('/', (req, res) => res.sendFile(__dirname + '/public/index.html'))
app.use(express.static('public'))
app.listen(port, () => console.log(`Listening on :${port}!`))


app.use('/', express.static(__dirname + '/public'))