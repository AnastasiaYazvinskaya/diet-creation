$(document).ready(function() {
    $(".drag").draggable({
        containment: "#container",
        //revert: valid,
        helper: "clone"
    });
    var item_order = new Array(3);
    for (var i = 0; i < item_order.length; i++) {
        item_order[i] = new Array(7);
    }
    $(".drop.type_1").droppable({
        accept: ".type_1",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.clone())
                .css("background-color", "rgb(195, 226, 192)");
            var day = $(this).attr("id");
            item_order[0][day] = ui.draggable.text();
                
            $("#check").html(ui.draggable.text())
            
            var order_string = 'order='+item_order;
            $.ajax({
                method: "POST",
                url: "/updateList",
                data: order_string,
                cache: false,
                success: function(data){    
                    $("#response").html(data);
                }
            });
        }
    });
    $(".drop.type_2").droppable({
        accept: ".type_2",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.clone())
                .css("background-color", "rgb(195, 226, 192)");

            var day = $(this).attr("id");
            item_order[1][day] = ui.draggable.text();
                    
            $("#check").html(ui.draggable.text())
                
            var order_string = 'order='+item_order;
            $.ajax({
                method: "POST",
                url: "/updateList",
                data: order_string,
                cache: false,
                success: function(data){    
                    $("#response").html(data);
                }
            });
        }
    });
    $(".drop.type_3").droppable({
        accept: ".type_3",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.clone())
                .css("background-color", "rgb(195, 226, 192)");

            var day = $(this).attr("id");
            item_order[2][day] = ui.draggable.text();
                
            $("#check").html(ui.draggable.text())
                
            var order_string = 'order='+item_order;
            $.ajax({
                method: "POST",
                url: "/updateList",
                data: order_string,
                cache: false,
                success: function(data){    
                    $("#response").html(data);
                }
            });
        }
    });

});