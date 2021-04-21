/*
*     Monitor V1
*     by : Emmett Cowan
*     FYP
*/
const express = require('express');
const port = process.env.PORT || 3000;
const path = require('path');
const passport = require('passport');
const bodyParser = require('body-parser');
const hbs = require('express-handlebars');

const app = express();


app.set('view engine', 'hbs');
app.engine("hbs",hbs({
    extname: "hbs",
    defaultLayout: false,
    layoutsDir: "views/layouts/"
  })
);
app.set('views', __dirname + '/views');
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(express.static(path.join(__dirname, 'public')));


// express session for saving cookie for user 
const expressSession = require('express-session')({
  secret: 'MoniorSecret',
  resave: false,
  saveUninitialized: false
});

app.use(expressSession);

//initilize passport & session
app.use(passport.initialize());
app.use(passport.session());

var routes = require('./routes/index');
app.use('/', routes);

//start listening for requests on port 
app.listen(port, () => console.log('app listening on port ' + port));


module.exports = app;