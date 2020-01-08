var spawn = require('child_process').spawn,
  py    = spawn('python3', ['main.py', "-W"]),
  data = {
  	"image_file": "uploads/dfsf",
  	"image_id": 123,
  	"user_id": 123,
  	"image_type": "skin"
  },
  dataString = '';

 /*Here we are saying that every time our node application 
 receives data from the python process output stream(on 'data'), 
 we want to convert that received data into a string and 
 append it to the overall dataString.*/
py.stdout.on('data', function(data){
  dataString += data.toString();
});

py.stderr.on('data', function(data){
  dataString += data.toString();
});

/*Once the stream is done (on 'end') we want to 
simply log the received data to the console.*/
py.stdout.on('end', function(){
  console.log('What we have',dataString);
});

/*We have to stringify the data first otherwise our python process wont recognize it*/
py.stdin.write(JSON.stringify(data));
console.log(JSON.stringify(data));

py.stdin.end();