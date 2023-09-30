const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
  // Get the requested URL
  const url = req.url === '/' ? '/index.html' : req.url;

  // Determine the file path based on the requested URL
  const filePath = path.join(__dirname, url);

  // Check if the file exists
  fs.exists(filePath, (exists) => {
    if (exists) {
      // Read the file and serve it as the response
      fs.readFile(filePath, (err, data) => {
        if (err) {
          res.writeHead(500, { 'Content-Type': 'text/plain' });
          res.end('Internal Server Error');
        } else {
          // Set the content type based on the file extension
          const ext = path.extname(filePath);
          const contentType = {
            '.html': 'text/html',
            '.css': 'text/css',
            '.js': 'text/javascript',
          }[ext] || 'text/plain';

          res.writeHead(200, { 'Content-Type': contentType });
          res.end(data);
        }
      });
    } else {
      // File not found
      res.writeHead(404, { 'Content-Type': 'text/html' });
      res.end('<h1>404 Not Found</h1>');
    }
  });
});

const port = process.env.PORT || 3000;
server.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
