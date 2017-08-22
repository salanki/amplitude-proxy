const Amplitude = require('amplitude');

const amplitude = new Amplitude(process.env.API_TOKEN);

const dgram = require('dgram');
const server = dgram.createSocket('udp4');

server.on('error', (err) => {
  console.log(`Listener error:\n${err.stack}`);
  server.close();
});

server.on('message', (msg, rinfo) => {
  console.log(`server got: ${msg.toString().trim()} from ${rinfo.address}:${rinfo.port}`);
  amplitude.track(JSON.parse(msg));
});

server.on('listening', () => {
  const address = server.address();
  console.log(`server listening ${address.address}:${address.port}`);
});

server.bind(process.env.LISTEN_PORT || 41255);