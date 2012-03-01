/* Imports */
var _ = require('underscore')
  , connect = require('connect')
  , everyauth = require('everyauth')
  , express = require('express')
  , path = require('path')
  , request = require('request')
  , qs = require('querystring');

/* Local Imports */
var conf = require('./conf');

var TEMPLATE_DIR = path.join(__dirname, 'views');

/* Debug info */
everyauth.debug = false;

/* Everyauth Stuff */
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
    user = usersById[++nextUserId] = {id: nextUserId, name:sourceUser.name};
    user[source] = sourceUser;
  }
  return user;
}

/* Find User */
everyauth.everymodule
  .findUserById( function (id, callback) {
    callback(null, usersById[id]);
  });

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
    res.render('index.jade', {});
  });

  app.post('/star/?', function(req, res) {
    console.log(req.user.id);
    console.log(req.body.star);
    console.log(req.body.id);
  });

  app.get('/wine/?', function(req, res) {
    res.render('wine/wine_list.jade', {
    });
  });

  app.get('/wine/:id', function(req, res) {
    res.render('wine/wine_detail.jade', {
      'wine_id': req.params.id,
    });
  });

  app.get('/search/?', function(req, res) {
    var q = req.query['q'];
    var product_url = 'https://www.googleapis.com/shopping/search/v1/public/products?'
    var product_qs = qs.stringify({
        "key": conf.goog.simpleApiKey,
        "country": 'US',
        "language": 'en',
        "currency": "USD",
        "spelling.enabled": true,
        "alt": 'json',
        "q": q,
    });
    var product = request.get(product_url + product_qs, function (e, r, body) {
        if (!e && r.statusCode == 200) {
          var results = JSON.parse(body);
          var spelling = _.map(results.spelling, function(item){
                return item;
          });
          if(!spelling.length)
            spelling = null;
          var items = _.map(results.items, function(item){
                return {
                  'id': item.id,
                  'title': item.product.title,
                  'description': item.product.description,
                  'link': item.product.link,
                  'brand': item.product.brand,
                  'image': _.first(item.product.images).link,
                  'price': _.first(item.product.inventories).price
                };
          });
          res.render('search.jade', {
            'products': items,
            'spelling': spelling
          });
        }
    });
  });

  /* helpers for everyauth */
  everyauth.helpExpress(app);

  app.listen(argv.p);
  console.log('Running your application on http://localhost:' + argv.p)
}
