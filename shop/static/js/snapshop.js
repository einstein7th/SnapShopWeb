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

    $('.remove-ingredient-list').click(function(event) {
	$("#"+$(this).data("containerid")).remove()
    });
    
    updateCart()
}

function getCart() {
    var cart = {}
    var cart_json = $('#id_items_list').val();
    if (cart_json.length > 0) {
        cart = $.parseJSON(cart_json);
        if (cart == null) {
            cart = {}
        }
    }
    return cart;
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

        total += element$.data("item-price");

        newRow$.append("<td>" + element$.data("item-name")+"</td>");
        newRow$.append('<td class="quantity">1</td>')
        newRow$.append("<td>$" + parseInt(element$.data("item-price"))/100.0+ "</td>");
        newRow$.append('<td><i class="icon-chevron-down"></i> <i class="icon-chevron-up"></i><i class="icon-remove"></i></td>')
        newRow$.attr('data-item-id', element$.data('item-id'));
        target$.append(newRow$);

        // Add listeners for icons:
    });

    $(".icon-chevron-up").click(function(event) {
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');
        var cart = getCart();

        if (cart.hasOwnProperty(item_id)) {
            cart[item_id] += 1;
        }

        console.log(cart);
        $('#id_items_list').val(JSON.stringify(cart));
        row$.children(".quantity").html(cart['' + item_id]);
    });

    $(".icon-chevron-down").click(function(event) {
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');
        var cart = getCart();

        if (cart.hasOwnProperty(item_id)) {
            if (cart[item_id] > 1) {
                cart[item_id] -= 1;
            } else if (cart[item_id] <= 1) {
                // Remove item basically. Deselect from area above to prevent future from clicks from bringing back
                $('*[data-item-id="' + item_id + '"]').removeClass('selected');
                row$.remove();
                delete cart[item_id];
            }

        }

        console.log(cart);
        $('#id_items_list').val(JSON.stringify(cart));
        row$.children(".quantity").html(cart['' + item_id]);
    });

    $(".icon-remove").click(function(event) {
        var row$ = $(this).parent().parent();
        var item_id = row$.data('item-id');
        var cart = getCart();

        if (cart.hasOwnProperty(item_id)) {
            // Remove item basically. Deselect from area above to prevent future from clicks from bringing back
            $('*[data-item-id="' + item_id + '"]').removeClass('selected');
            row$.remove();
            delete cart[item_id];
        }

        console.log(cart);
        $('#id_items_list').val(JSON.stringify(cart));
        row$.children(".quantity").html(cart['' + item_id]);
    });

    var element$ = $(clickedElement);
    // Add cart item to purchase form, which is a hidden input field
    var cart = getCart();

    var item_id = element$.data("item-id");

    console.log("item another item with id: " + item_id);

    if (cart.hasOwnProperty(item_id)) {
        // Clicking an item again toggles/removes it from cart
        if (cart[item_id] > 0) {
            cart[item_id] = 0;
        } else {
            cart[item_id] = 1;
        }
    } else {
        cart['' + item_id] = 1;
    }

    $('#id_items_list').val(JSON.stringify(cart));

    // Send cart change to server, which will save it
    $.ajax({
        url: "/save_cart/",
        data: JSON.stringify(cart)
    }).done(function() {
        console.log('done saving cart')
    })
}

$(document).ready(init);
