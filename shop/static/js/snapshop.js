cart = []

function init() {
    $('.tooltipped').tooltip();
    $('.half-height').each(function(index,element) {
    var targetHeight =  $(element).height();
    var parentHeight = $(element).parent().height();

    $(element).css("position","relative");
    $(element).css("top",(parentHeight-targetHeight)/2)
    $(element).css("margin-top",0)
    $(element).css("margin-bottom",0)

    });

    $('.ingredient-list .ingredient-item').click(function(event) {
        $(this).toggleClass("selected");
        updateCart(this);
    });
    
    updateCart()
}

function updateCart(clickedElement) {
    var target$ = $("#cart-table tbody");
    var total = 0;

    if ($('.ingredient-list .ingredient-item.selected').length==0) {
	target$.append("<td colspan='4'>You currently have no items in your cart")
    }

    $('.ingredient-list .ingredient-item.selected').each(function(index,element) {
        // Add cart item to visible cart
        var element$ = $(element);
        var newRow$ = $('<tr>');

        total+=element$.data("item-price");

        newRow$.append("<td>" + element$.data("item-name")+"</td>");
        newRow$.append("<td>1</td>")
        newRow$.append("<td>$" + parseInt(element$.data("item-price"))/100.0+ "</td>");
        newRow$.append("<td></td>")
        target$.append(newRow$);
    });

    var element$ = $(clickedElement);
    // Add cart item to purchase form, which is a hidden input field
    var cart = {}
    var cart_json = $('#id_items_list').val();
    if (cart_json.length > 0) {
        cart = $.parseJSON(cart_json);
        if (cart == null) {
            cart = {}
        }
    }

    var item_id = element$.data("item-id");
    console.log("item another item with id: " + item_id);
    if (cart.hasOwnProperty(item_id)) {
        // Clicking an item again toggles/removes it from cart
        if (cart['' + item_id] > 0) {
            cart['' + item_id] = 0;
        } else {
            cart['' + item_id] = 1;
        }

        // incrementing count:
        //cart['' + item_id] = parseInt(cart['' + item_id], 10) + 1;
    } else {
        cart['' + item_id] = 1;
    }

    $('#id_items_list').val(JSON.stringify(cart));

    // Send cart change to server, which will save it
    // TODO
}

$(document).ready(init);
