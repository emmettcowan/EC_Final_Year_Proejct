const express = require('express');
const app = express();
const port = process.env.PORT || 3000;
const passport = require('passport');
const mongoose = require('mongoose');
const passportLocalMongoose = require('passport-local-mongoose');
const connectEnsureLogin = require('connect-ensure-login');
var hbs  = require('express-handlebars');



app.use(express.static(__dirname ));

app.engine('handlebars', hbs());
app.set('view engine', 'handlebars');

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
mongoose.connect('mongodb://localhost/MyDatabase',
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
  
        return res.redirect('/');
      });
  
    })(req, res, next);
  });

app.get('/login',
  (req, res) => res.render('index', {name: "john"})
);

app.get('/',
  connectEnsureLogin.ensureLoggedIn(),
  (req, res) => res.sendFile('html/index.hbs', {name: 'john'})
);

app.get('/private',
  connectEnsureLogin.ensureLoggedIn(),
  (req, res) => res.sendFile('html/private.hbs', {root: __dirname})
);

app.get('/user',
  connectEnsureLogin.ensureLoggedIn(),
  (req, res) => res.send({user: req.user})
);

