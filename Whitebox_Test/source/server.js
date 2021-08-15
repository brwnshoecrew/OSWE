const child_process = require('child_process');

var express = require('express');
const bodyParser = require("body-parser");
var app = express();

app.set("view engine", "pug");
app.set("views", __dirname + '/views');

app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static(__dirname + '/css'));

const host = '0.0.0.0';
const port = 21440;

app.get('/', function (req, res) {
    res.render("index");
})

app.get("/source.zip", (req, res) => {
    res.download('./source.zip');
})

app.post('/whoami', function (req, res) {
    try {
        child_process.exec(
            'whoami',
            function (error, stdout) {
                if (error) {
                    console.log('error: ', error);
                }
                res.render("index", { response: stdout });
                res.end();
            });
    }
    catch (e) {
        res.render("index", { response: 'something went wrong!' });
        res.end();
    }
})

app.post('/hostname', function (req, res) {
    try {
        eval('child_process.exec("hostname",function (error, stdout) {res.render("index", { response: stdout });});');
    }
    catch (e) {
        res.render("index", { response: 'something went wrong!' });
        res.end();
    }
})

app.post('/ifconfig', function (req, res) {
    try {
        child_process.execFile(
            'ifconfig',
            [(req.body.iface != null) ? req.body.iface : '-a'],
            function (error, stdout) {
                res.render("index", { response: stdout });
                res.end();
            });
    }
    catch (e) {
        res.render("index", { response: 'something went wrong!' });
        res.end();
    }
})

app.post('/ping', function (req, res) {
    try {
        console.log('Got to /ping');
        console.log(req.body.ip)
        console.log("Passed")
        child_process.execFile(
            'ping',
            ['-c 1',
                (req.body.debug == 'true') ?
                    //((req.body.ip != null) && eval(`ip = JSON.parse('{"ip":"1"}'); console.log('injection');//').ip;`) !== "undefined") ?
                    ((req.body.ip != null) && eval(`ip = JSON.parse('${req.body.ip}').ip;`) !== "undefined") ?
                        ip : '127.0.0.1' : '127.0.0.1'],
            function (error, stdout) {
                res.render("index", { response: stdout });
                res.end();
            });
            result = child_process.execFile(
                'ping',
                ['-c 1',
                    (req.body.debug == 'true') ?
                        ((req.body.ip != null) && eval(`ip = JSON.parse('${req.body.ip}').ip;`) !== "undefined") ?
                            ip : '127.0.0.1' : '127.0.0.1'],
                function (error, stdout) {
                    res.render("index", { response: stdout });
                    res.end();
                });
            //console.log(result);
            console.log(req.body.ip);
            console.log('Got to end of child_process');
    }
    catch (e) {
        console.log('Got to catch statement...');
        res.render("index", { response: 'something went wrong!' });
        res.end();
    }
})

app.listen(port, host, function () {
    console.log(`Server is running on http://${host}:${port}`);
})
