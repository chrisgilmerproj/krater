/* Imports */
var _ = require('underscore')
  , cons = require('consolidate')
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
ratings_debug = false;

/* Ratings data */
var ratings = {};
var wine_data = {};

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
  app.engine('jade', cons.swig);
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
    if(!_.has(ratings, req.user.id))
      ratings[req.user.id] = {};
    ratings[req.user.id][req.body.id] = req.body.star;
    if(ratings_debug)
      console.log(JSON.stringify(ratings));
  });

  app.get('/wine/?', function(req, res) {
    var results = [];
    if (req.user){
      user_ratings = ratings[req.user.id]
      if(!_.isEmpty(user_ratings)){
        var results = _.map(_.keys(user_ratings), function(item){
          var thing = wine_data[item];
          if(thing){
            thing['rating'] = user_ratings[item];
          }
          return thing;
        });
      }
    }
    res.render('wine_list.jade', {
      "products": results,
    });
  });

  app.get('/search/?', function(req, res) {
    var q = req.query.q || null;
    var product_url = 'https://www.googleapis.com/shopping/search/v1/public/products?'
    var product_qs = qs.stringify({
        "key": conf.goog.simpleApiKey,
        "country": 'US',
        "language": 'en',
        "currency": "USD",
        "rankBy": "relevancy",
        "spelling.enabled": true,
        "crowdBy": "brand:1",
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
                var wine = {
                  'id': item.id,
                  'title': item.product.title,
                  'description': item.product.description,
                  'link': item.product.link,
                  'brand': item.product.brand,
                  'image': _.first(item.product.images).link,
                  'price': _.first(item.product.inventories).price,
                  'rating': null,
                };
                wine_data[item.id] = wine
                return wine
          });
          res.render('search.jade', {
            'query': q,
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
