var express = require('express');
var router = express.Router();
var mongoose = require('mongoose');
mongoose.connect('localhost:27017/scriptDb');
var Schema = mongoose.Schema;

var userDataSchema = new Schema({
  Name: String,
  Script: String
});

var UserData = mongoose.model('script', userDataSchema);

router.get('/', function(req, res, next) {
  UserData.find()
      .then(function(doc) {
        console.log("Got as far as here, array length is: " + doc.length);
        res.render('index', {title: "Moniter", items: doc});
      });
});

module.exports = router;
