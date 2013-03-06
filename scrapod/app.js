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

app.get("/",function(req,res) {
    res.end("dobby not so smart");
})

app.get('/search/:query/', function(req, res){
    var searchQuery = req.params['query'];    

    request({
	uri: "http://www.peapod.com/search_results.jhtml?_D%3AsearchText=+&x=22&y=12&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brandId=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brandId=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.categoryId=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.categoryId=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.catNodeId=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.catNodeId=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brand=&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.brand=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.category=&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.category=+&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.search=0&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.search=+&start=1&sort=-searchScore%2C-userFrequency%2C-itemsPurchased&%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.storeId=2&_D%3A%2Fpeapod%2Fhandler%2Fiditarod%2FSearchHandler.storeId=+&results=standard&typeahead=0&_DARGS=%2Ffr4_top.jhtml&searchText="+searchQuery,
	headers: {
	    "Cookie":"v1st=5F9397A0EC690852; __qca=P0-272779979-1362371386534; RES_TRACKINGID=75207680595717326; stype=1; RES_SESSIONID=29810795656565526; ResonanceSegment=1; JSESSIONID=H5TSIZ0HGAHAICQBD0WSF3Q; peapodCookie20=-4e6dfb23%3a13d3a59e19b%3a6c83ad0a1enNq; tmdts=1; __utmz=17384120.1362556763.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=17384120.3083127514490278000.1362556763.1362556763.1362556763.1; __utmc=17384120; __utmb=17384120.1.10.1362556763"
	}
    }, function(err, response, body){
        var self = this;
        if(err && response.statusCode !== 200){console.log('Request error.');}
	
	
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
