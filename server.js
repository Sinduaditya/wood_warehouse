const http = require('http');

http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/html'});
    res.write('Hello World!<br>');
    res.write('This is Andini Maharani Putri');
    res.end();
}).listen(8080, () => {
    console.log('Server running at http://localhost:8080');
});