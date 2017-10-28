var ip = process.argv[2];
var port = process.argv[3];
console.log("Connect to REDIS " + ip + ":" + port);

var express = require('express');
var app = express();
app.use(function(req, res, next) {
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "X-Requested-With");
        res.header("Access-Control-Allow-Headers", "Content-Type");
        res.header("Access-Control-Allow-Methods", "PUT, GET, POST, DELETE, OPTIONS");
        next();
    });
var server = require('http').createServer(app);
var io = require('socket.io')(server);
var redis = require('redis');
 
io.set('origins', '*:*');

var redisClient = redis.createClient(port, ip, {no_ready_check: true});
// redisClient.auth('axhPJvd7NKQQLNMK', function (err) {
//   console.log(err);
// });
redisClient.subscribe('new-case');

redisClient.on("message", function(channel, message) {
  try {
    console.log(message);
    var data = JSON.parse(message);
    // io.to("1").emit("1", data);
    io.emit('new_case', data.data);
  } catch(err) {
    console.log(err);
  }
});

redisClient.on("error", function(err){
  console.error("Error Redis: ", err);
});

server.listen(8890);
