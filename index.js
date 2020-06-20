const path = require('path');
const express = require('express');
const http = require("http")
const WebSocket = require('ws');

const app = express();

const HTTP_PORT = process.env.PORT || 3000;
// For authentication token look at the environment variable.
const ROBOT_AUTH_TOKEN = process.env.ROBOT_AUTH_TOKEN || "";

/////////////////////////////////////
// HTTP stuff
/////////////////////////////////////

app.get('/client', (req, res) => res.sendFile(path.resolve(__dirname, './client.html')));
app.get('/streamer', (req, res) => res.sendFile(path.resolve(__dirname, './streamer.html')));
app.get('/controller', (req, res) => res.sendFile(path.resolve(__dirname, './controller.html')));

const server = http.createServer(app);
server.listen(HTTP_PORT);

console.log(`HTTP server listening at http://localhost:${HTTP_PORT}`);

/////////////////////////////////////
// Web sockets
/////////////////////////////////////

const wsServer = new WebSocket.Server({server: server}, () => 
	console.log(`WS server is listening at ws://localhost:${HTTP_PORT}`));

// array of connected websocket clients
let connectedClients = [];

var iter = 0;

wsServer.on('connection', (ws, req) => {
	console.log("Attempt connection");
	token = req.headers['sec-websocket-protocol'];

	if (ROBOT_AUTH_TOKEN.length > 10 && token === ROBOT_AUTH_TOKEN) {
		//now is authenticated
		console.log('Connected client');
	    // add new connected client
	    connectedClients.push(ws);
	    console.log('Total connected = ' + connectedClients.length);
	}

	ws.on('message', data => {
		console.log(iter);
		iter += 1;
    	// listen for messages from the streamer, the clients will not send anything so we don't need to filter
    	if (connectedClients.indexOf(ws) >= 0) {
	        // send the base64 encoded frame to each connected ws
	        connectedClients.forEach((open_ws, i) => {
	            if (open_ws.readyState === open_ws.OPEN) { // check if it is still connected
	            	if (open_ws !== ws) {
	                	open_ws.send(data); // send
	            	}
	            } else { // if it's not connected remove from the array of connected ws
	                connectedClients.splice(i, 1);
	            }
	        });
	    }
    });

});