/*
*     Monitor V0.7
*     by : Emmett Cowan
*     FYP
*/
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const passport = require('passport');
const mongoose = require('mongoose');
const passportLocalMongoose = require('passport-local-mongoose');
const connectEnsureLogin = require('connect-ensure-login');
const path = require('path');
var data;


var hbs  = require('express-handlebars');
app.set('view engine', 'hbs');
app.engine("hbs",hbs({
    extname: "hbs",
    defaultLayout: false,
    layoutsDir: "views/layouts/"
  })
);

app.set('views', __dirname + '/views');

app.use(express.static(path.join(__dirname, 'public')));

//bodyparser for extracitng infor out of the body of the request
// express session for saving cookie for user 
const bodyParser = require('body-parser');
const expressSession = require('express-session')({
    secret: 'MoniorSecret',
    resave: false, 
    saveUninitialized: false
});

app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(expressSession);

//start listening for requests on port 
app.listen(port, () => console.log('app listening on port ' + port));

//initilize passport & session
app.use(passport.initialize());
app.use(passport.session());

//connect to user db and setup schema
mongoose.connect('mongodb://localhost/users',
  { useNewUrlParser: true, useUnifiedTopology: true });

const Schema = mongoose.Schema;
const UserDetail = new Schema({
  username: String,
  password: String
});

//Sets up passport with local startagy and also adds salt/hash keys to out db schema for encription
UserDetail.plugin(passportLocalMongoose);
const UserDetails = mongoose.model('userInfo', UserDetail, 'userInfo');

passport.use(UserDetails.createStrategy());

passport.serializeUser(UserDetails.serializeUser());
passport.deserializeUser(UserDetails.deserializeUser());

app.post('/login', (req, res, next) => {
    passport.authenticate('local',
    (err, user, info) => {
      if (err) {
        return next(err);
      }
  
      if (!user) {
        return res.redirect('/login?info=' + info);
      }
  
      req.logIn(user, function(err) {
        if (err) {
          return next(err);
        }

        var MongoClient = require('mongodb').MongoClient;
        var url = "mongodb://localhost:27017/";


        MongoClient.connect(url, function(err, db) {
        if (err) throw err;
        var dbo = db.db("Monitor");
        dbo.collection(req.user.username).find({}).toArray(function(err, result) {
            if (err) throw err;
            data = JSON.stringify(result);
            //console.log(result);
            db.close();
            });
        });

        return res.redirect('/dashboard');
      });
  
    })(req, res, next);
});



app.get('/logout', function(req, res){
  req.logout();
  res.redirect('/');
});

app.post('/register', (req, res, next) => {
  UserDetails.register({username: req.body.name, active: false}, req.body.password);
  return res.redirect('/login');
});

app.get('/login',
  (req, res) => res.render('login')
);

app.get('/register',
  (req, res) => res.render('register')
);

app.get("/about",
(req, res) => res.render('about'))

app.get('/',
  (req, res) => res.render('index')
);

app.get('/contact',
  (req, res) => res.render('contact')
);

app.get('/dashboard',
  connectEnsureLogin.ensureLoggedIn(),
  (req, res) => res.render('dashboard', { name : req.user.username, data: data})
);

app.get('/private',
  connectEnsureLogin.ensureLoggedIn(),
  (req, res) => res.render('private', { name : req.user.username})
);

// app.get('/user',
//   connectEnsureLogin.ensureLoggedIn(),
//   (req, res) => res.send({user: req.user})
// );

