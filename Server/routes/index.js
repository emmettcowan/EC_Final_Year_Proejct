var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
mongoose.connect('localhost:27017/Monitor');
var Schema = mongoose.Schema;

var userDataSchema = new Schema({
  _id: String,
  User: String,
  App: String,
  Date: String,
  Time: Number
});



var UserData = mongoose.model('Monitor', userDataSchema);

router.get('/', function(req, res, next) {
  UserData.find()
      .then(function(doc) {
        console.log("Got as far as here, array length is: " + doc.length);
        res.render('index', {title: "Monitor", items: doc});
      });
});

router.post('/getDb', function(req, res, next){
  Monitor.find()
      .then(function(doc){
        res.render('index', {title: "Monitor", db:" doc"})
      });
});



module.exports = router;
