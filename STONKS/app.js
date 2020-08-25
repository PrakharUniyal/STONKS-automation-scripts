const express = require('express');
const bodyParser = require("body-parser");

const fs = require('fs');

const sheetsAuth = require('./sheetsAuth');
const { google } = require('googleapis');

const gameData = require('./gameData');

const app = express();
app.use(bodyParser.urlencoded({ extended: false }));

var sheets;
fs.readFile('credentials.json', (err, content) => {
    if (err) return console.log('Error loading client secret file:', err);
    // Authorize a client with credentials, then call the Google Sheets API.
    sheetsAuth.authorize(JSON.parse(content),function(auth) {
        sheets = google.sheets({version: 'v4', auth});
    });
});

const spreadsheetId = '1viltXrvJSsCW6-Mn9-uP_6PqF2whNXScdan6CFaLXok';

app.get('/',function(req,res) {
    res.send('Welcome!');
})

app.get('/team',function(req,res) {
    var x = {};
    sheets.spreadsheets.values.get({
        spreadsheetId: spreadsheetId, 
        range: req.query.name+'!A1:K12'
    }, 
    (err, sres) => {
        if (err) {
            res.send('There is something wrong with the team name.'); 
            return console.log('The API returned an error: ' + err);
        }
        const rows = sres.data.values;
        if (rows.length) {
            rows.map((row) => {
                x[`${row[0]}`]=`${row[1]}`;
            });
        } else {
            x["msg"]='No data found.';
        }
        res.send(x);
    });    
})

app.get('/valUpdate', function(req,res) {
    res.sendFile('/static/update.html', { root: __dirname });
})

app.post('/valUpdate',function(req,res) {
    var team = gameData.playerData[req.body.pName][0];
    var index = gameData.playerData[req.body.pName][1];
    var newVal = Number(req.body.val);

    let values = [
        [
            newVal
        ],
    ];

    var resource = {
        values,
    };

    sheets.spreadsheets.values.update({
        spreadsheetId: spreadsheetId,
        range: team+'!C'+index,
        valueInputOption: 'RAW',
        resource: resource,
    }, (err, result) => {
        if (err) {
            console.log(err);
        } else {
            console.log('Cell updated.');
        }
    });
    
    res.send('Updated');
})

app.listen(3000);
