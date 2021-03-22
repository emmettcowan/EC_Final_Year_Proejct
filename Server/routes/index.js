var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
const passport = require('passport');
const passportLocalMongoose = require('passport-local-mongoose');
const connectEnsureLogin = require('connect-ensure-login');

var chartData =[];
var headingData = [];

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

router.post('/login', (req, res, next) => {
    passport.authenticate('local', { successReturnToOrRedirect: '/dashboard', failureRedirect: '/login' },
        (err, user, info) => {
            if (err) {
                return next(err);
            }

            if (!user) {
                return res.redirect('/login?info=' + info);
            }

            req.logIn(user, function (err) {
                if (err) {
                    return next(err);
                }

                var MongoClient = require('mongodb').MongoClient;
                var url = "mongodb://localhost:27017/";


                MongoClient.connect(url, function (err, db) {
                    if (err) throw err;
                    var dbo = db.db("Monitor");
                    dbo.collection(req.user.username).find({}).toArray(function (err, result) {
                        if (err) throw err;
                        console.log(result);
                        // for (i = 0; i < result.length; i++) {
                        //     headingData.push(result[i].App);
                        //     chartData.push(result[i].Total_time);
                        // }
                        // console.log(headingData);
                        // console.log(chartData);
                        chartData = JSON.stringify(result);
                        db.close();
                    });
                });

                return res.redirect('/dashboard');
            });

        })(req, res, next);
});



router.get('/logout', function (req, res) {
    req.logout();
    res.redirect('/');
});

router.post('/register', (req, res, next) => {
    var username = req.body.name
    UserDetails.register({ username: username, active: false }, req.body.password);
    return res.redirect('/login');
});

router.get('/login',
    (req, res) => res.render('login')
);

router.get('/register',
    (req, res) => res.render('register')
);

router.get("/about",
    (req, res) => res.render('about'))

router.get('/',
    (req, res) => res.render('index')
);

router.get('/contact',
    (req, res) => res.render('contact')
);

router.get('/dashboard',
    connectEnsureLogin.ensureLoggedIn(),
    (req, res) => res.render('dashboard', { name: req.user.username, chartData: chartData, headingData: headingData })
);

router.get('/private',
    connectEnsureLogin.ensureLoggedIn(),
    (req, res) => res.render('private', { name: req.user.username })
);


module.exports = router;