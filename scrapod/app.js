var express = require('express')
, jsdom = require('jsdom')
, request = require('request')
, url = require('url')
, http = require('http');

var app = express();

app.configure(function(){
    app.set('port', process.env.PORT || 3000);
    app.use(express.bodyParser());
    app.use(express.methodOverride());
});

session = ""
cookie = ""
peapodcookie=""

function refreshSession() {
    request.post({
	uri : "http://www.peapod.com/site/gateway/zip-entry/top/zipEntry_main.jsp?_DARGS=/site/gateway/zip-entry/top/zipEntry_main.jsp",
	form : {
	    "_dyncharset": "ASCII",
	    "/peapod/handler/iditarod/ZipHandler.continueURL":"/site/gateway/zip-entry/top/selectCity.jsp?NUM1=1361081670096",
	    "_D:/peapod/handler/iditarod/ZipHandler.continueURL": "",
	    "/peapod/handler/iditarod/ZipHandler.submitSuccessURL": "/site/gateway/zip-entry/top/zipEntry_main.jsp?NUM1=1361081670096",
	    "_D:/peapod/handler/iditarod/ZipHandler.submitSuccessURL": "",
	    "/peapod/handler/iditarod/ZipHandler.submitFailureURL": "/site/gateway/zip-entry/top/zipEntry_main.jsp?NUM1=1361081670096",
	    "_D:/peapod/handler/iditarod/ZipHandler.submitFailureURL": "",
	    "zipcode": "02139",
	    "_D:zipcode": "",
	    "/peapod/handler/iditarod/ZipHandler.collectProspectURL" : "/site/gateway/zip-entry/top/collectProspect.jsp",
	    "_D:/peapod/handler/iditarod/ZipHandler.collectProspectURL": "",
	    "/peapod/handler/iditarod/ZipHandler.storeClosedURL": "/site/gateway/zip-entry/top/storeClosed.jsp",
	    "_D:/peapod/handler/iditarod/ZipHandler.storeClosedURL": "",
	    "/peapod/handler/iditarod/ZipHandler.defaultGuestParameters": "true",
	    "_D:/peapod/handler/iditarod/ZipHandler.defaultGuestParameters": "",
	    "memberType": "C",
	    "_D:memberType": "",
	    "_D:memberType": "",
	    "Continue": "Create Account",
	    "_D:Continue": "",
	    "_DARGS": "/site/gateway/zip-entry/top/zipEntry_main.jsp"
	}
    }, function (err,response,body) {
	console.log(response.headers);
	cookie = response.headers['set-cookie'][0].split(";")[0];
	session = response.headers['set-cookie'][1].split(";")[0].split("JSESSIONID=")[1];
	peapodcookie = response.headers['set-cookie'][2].split(";")[0].split("peapodCookie20=")[1];

	console.log(cookie);
	console.log(session);
	console.log(peapodcookie);
	
	if (!err && response.statusCode == 200) {
	    console.log("success")
            console.log(body)
        } else {
	    console.log("errror")
	    console.log(err);
	}
	})
}

function refreshSessionContinue() {
    refreshSession();
    setTimeout(refreshSessionContinue,60000);
}

refreshSessionContinue();

app.get("/",function(req,res) {
    res.end("dobby not so smart");
})

app.get('/search/:query/', function(req, res){
    var searchQuery = req.params['query'];    

    request({
	uri: "http://www.peapod.com/search_results.jhtml?_D%3AsearchText=+&x=22&y=12&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brandId=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brandId=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.categoryId=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.categoryId=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.catNodeId=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.catNodeId=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brand=&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brand=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.category=&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.category=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.search=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.search=+&start=1&sort=-searchScore%2C-userFrequency%2C-itemsPurchased&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.storeId=2&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.storeId=+&results=standard&typeahead=0&_DARGS=%2Ffr4_top.jhtml&searchText="+searchQuery,
	headers: {
	    "Cookie":cookie+"; JESSIONID=" + session + "; peapodCookie20="+peapodcookie + ";"
	}
    }, function(err, response, body){
        var self = this;
        if(err && response.statusCode !== 200){console.log('Request error.');}
	console.log(err);
	
	
	jsdom.env({
            html: body,
            scripts: ["http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"]
        }, function(err, window){
            res.writeHead(200, { 'Content-Type': 'application/json' });
	    console.log(body)

            var $ = window.jQuery;	    
	    output = {'count':0,'results':[]}
	    $('.SRProductsGridItemDesc').each(function(index,element) {
		output['count']++;
		output['results'].push(element.textContent.trim());
	    })
	    res.end(JSON.stringify(output))
	})
    });
});

http.createServer(app).listen(app.get('port'), function(){
    console.log("Express server listening on port " + app.get('port'));
});
