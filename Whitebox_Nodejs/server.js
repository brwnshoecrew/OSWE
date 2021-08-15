const http = require('http');
const { validateKey } = require("./validateKey.js");
const fs = require('fs').promises;

const host = '0.0.0.0';
const port = 21440;

function deniedPage(res) {
    fs.readFile(__dirname + "/denied.html")
        .then(contents => {
            res.setHeader("Content-Type", "text/html");
            res.writeHead(403);
            res.end(contents);
        })
        .catch(err => {
            res.writeHead(500);
            res.end(err);
            return;
        });
}

function adminPage(res) {
    fs.readFile(__dirname + "/admin.html")
        .then(contents => {
            res.setHeader("Content-Type", "text/html");
            res.writeHead(200);
            res.end(contents);
        })
        .catch(err => {
            res.writeHead(500);
            res.end(err);
            return;
        });
}

var server = http.createServer(function (req, res) {
    if (req.url == '/') {
        res.writeHead(200);
        res.end();
    }
    else if (req.url == '/admin') {
        console.log("Reached /admin");
        if (req.method == 'POST') {
            console.log("Sent POST");
            var body = '';
            req.on('data', function (data) {
                body += data;
            })
            req.on('end', function () {
                if (validateKey(body)) {
                    adminPage(res);
                }
                else {
                    deniedPage(res);
                }
            })
        }
        else {
            deniedPage(res);
        }
    }
    else {
        res.writeHead(404);
        res.end('Page Not Found');
    }
});

server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
});
