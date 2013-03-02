
function init() {
    $('.half-height').each(function(index,element) {
	var targetHeight =  $(element).height();
	var parentHeight = $(element).parent().height();
	
	$(element).css("position","relative");
	$(element).css("top",(parentHeight-targetHeight)/2)
	$(element).css("margin-top",0)
	$(element).css("margin-bottom",0)
		
    });
}

$(document).ready(init);
