var optimist = require('optimist')
  , path = require('path');

var app = require('./web/app');                                                                                
                                                                                                               
exports.run = function() {                                                                                     
  var argv;                                                                                            
                                                                                                               
  optimist = optimist.usage('Usage: $0 -p [port] [-h]');                        
  optimist = optimist['default']('p', 3000);                                                                   
  optimist = optimist['default']('h', false);                                                                  
  optimist = optimist.alias('h', 'help');                                                                      
  optimist = optimist.describe('h', 'Print usage help');                        
  argv = optimist.argv;                                                                                        
                                                                                                               
  if (argv.h) {                                                                                                
    optimist.showHelp(console.log);                                                                            
  } else {                                                                                                     
    app.run(argv);                                                                                             
  }                                                                                                            
} 
