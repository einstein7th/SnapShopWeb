
function init() {
    $('.half-height').each(function(index,element) {
	var targetHeight =  $(element).height();
	var parentHeight = $(element).parent().height();
	
	$(element).css("position","relative");
	$(element).css("top",(parentHeight-targetHeight)/3)
		
    });
}

$(document).ready(init);
