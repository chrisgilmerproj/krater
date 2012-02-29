/* Imports */
var conf = require('./conf')
  , connect = require('connect')
  , everyauth = require('everyauth')
  , express = require('express')
  , path = require('path');

var TEMPLATE_DIR = path.join(__dirname, 'views');

/* Everyauth Stuff */
everyauth.debug = true;

/* User info */
var nextUserId = 0;
var usersById = {};
var usersByType = {
    'facebook': {},
    'twitter': {},
};

function addUser (source, sourceUser) {
  var user;
  if (arguments.length === 1) { // password-based
    user = sourceUser = source;
    user.id = ++nextUserId;
    return usersById[nextUserId] = user;
  } else { // non-password-based
    user = usersById[++nextUserId] = {id: nextUserId};
    user[source] = sourceUser;
  }
  return user;
}

/* Facebook Connection */
everyauth.facebook
  .appId(conf.fb.appId)
  .appSecret(conf.fb.appSecret)
  .findOrCreateUser( function (session, accessToken, accessTokenExtra, fbUserMetadata) {
    return usersByType['facebook'][fbUserMetadata.id] ||
      (usersByType['facebook'][fbUserMetadata.id] = addUser('facebook', fbUserMetadata));
  })
  .redirectPath('/');

/* Twitter Connection */
everyauth.twitter
  .consumerKey(conf.twit.consumerKey)
  .consumerSecret(conf.twit.consumerSecret)
  .findOrCreateUser( function (sess, accessToken, accessSecret, twitUser) {
    return usersByType['twitter'][twitUser.id] || (usersByType['twitter'][twitUser.id] = addUser('twitter', twitUser));
  })
  .redirectPath('/');

/* The Express App */
exports.run = function(argv) {
  /* create the server */
  var app = express.createServer(
      express.bodyParser()
    , express.favicon() // TODO: Need to get a favicon and fill this out
    , express.cookieParser()
    , express.session({ secret: 'somesecretword'})
    , everyauth.middleware()
  );

  /* setup templating engine */
  app.configure( function() {
    app.set('views', TEMPLATE_DIR);
    app.set('view engine', 'jade');
    app.set('view options', {layout: false});
  });

  /* setup middleware */                                                                                       
  app.use('/static', express.static(path.join(__dirname, '..', '..', 'extern')));
  app.use('/static', express.static(path.join(__dirname, '..', '..', 'static')));

  app.get('/', function(req, res) {
    res.render('index.jade', {
      'nextUserId': nextUserId,
      'usersById': usersById,
      'usersByType': usersByType,
    });
  });

  /* helpers for everyauth */
  everyauth.helpExpress(app);

  app.listen(argv.p);
  console.log('Running your application on http://localhost:' + argv.p)
}
