function count_items(list, item){
    count = 0;
    for (let i=0; i<list.length; i++){
        if (list[i] == item){
            count += 1;
        }
    }
    return count;
}

/* Menu page (menu.html) */
$(document).ready(function() {
    var num = 0;
    // Data for creation product list
    var prod_list = [$("#menu-id").text()];
    // List of weeks for product list
    var week = [];
    // Choose weeks number
    $(".weeks-choose").click(function() {
        // Clear data for product list (save just menu ID)
        prod_list = [prod_list[0]];
        // Change style for choosen variant
        $(this).css({"color":"#00994d",
                     "font-weight":"bold"});
        // Save choosen number of weeks for product list
        num = $(this).attr('id').slice(-1);
        // Add choosen number of weeks into the data for product list creation
        prod_list.push(num);
        // Clear style for all buttons except choosen
        for (let k=1; k<=4; k++){
            if (k != num){
                $("#list_"+k).css({"color":"#000",
                                   "font-weight":"normal"});
            }
            $("#list-choose_"+k).css({"color":"#000",
                                      "font-weight":"normal"});
        }
        // Clear superscripts
        $("sup").html("").css({"border": "none"});
        // Clear product list
        $(".products-list-2").html("<ul class='list-group list-group-flush'>"+
        "<li class='list-group-item d-flex justify-content-between align-items-center' style='font-weight: bold; background-color: rgb(231, 231, 231);'>Total price"+
        "<div><span class='badge badge-warning badge-pill'></span></div></li></ul>");
        
        // Show product list data into the 'check' place
        //$("#check").html(prod_list);
        // Choose concreete weeks for product list
        if (weeks_num != '1'){
            // Show possible weeks for choose
            $(".choose-week-btns").show();
        }
        // List of weeks for product list
        week = [];
    });

    $(".week-choose").click(function(){
        // Change style for clicked week (bold dark-green)
        $(this).css({"color":"#00994d",
                     "font-weight":"bold"});
        // Clear product list data
        if (prod_list.length > 2) {
            prod_list.pop();
        }
        // Product list for 1(one) week
        if (num == 1){
            // Clear weeks list
            if (week.length == 1){
                week.pop();
            }
            // Add choosen week to the weeks list
            week.push($(this).attr('id').slice(-1));
            // Clear style for 
            for (let k=1; k<=4; k++){
                if (!week.includes(String(k))){
                    $("#list-choose_"+k).css({"color":"#000",
                                    "font-weight":"normal"});
                }
            }
        }
        // Product list for 2(two) weeks
        else if (num == 2){
            // Add the same week (second of same type)
            if (week.length == 1 && $(this).attr('id').slice(-1) == week[0]){
                week.push($(this).attr('id').slice(-1));
            }
            // Delete week if it was clicked but it is already two of them in the list
            else if (week.length == 2 && week.includes($(this).attr('id').slice(-1))){
                week.splice(week.indexOf($(this).attr('id').slice(-1)), 1);
            }
            // Add new week
            else if (week.length < 2){
                week.push($(this).attr('id').slice(-1));
            }
            // Add sup if there are two this week
            if (count_items(week, $(this).attr('id').slice(-1)) == 2){
                $(this).children("sup").html("2").css({"padding": "0 4px",
                                                       "border":"1px solid #000",
                                                       "border-radius": "50%"});
            }
            // Delete sup if there is just one this week
            else {
                $(this).children("sup").html("").css({"border": "none"});
            }
            // Clear style if it was deleted from the week list
            if (!week.includes($(this).attr('id').slice(-1))){
                $(this).css({"color":"#000",
                             "font-weight":"normal"});
            }
        }
        // Product list for 3(three) weeks
        else if (num == 3){
            // Add the same week (second of same type)
            if (week.length == 1 && $(this).attr('id').slice(-1) == week[0]){
                week.push($(this).attr('id').slice(-1));
            }
            // Add the same week (third of same type)
            else if (week.length == 2 && $(this).attr('id').slice(-1) == week[0] && $(this).attr('id').slice(-1) == week[1]){
                week.push($(this).attr('id').slice(-1));
            }
            // Delete week if it was clicked but it is already three of them in the list
            else if (week.length == 3 && week.includes($(this).attr('id').slice(-1))){
                week.splice(week.indexOf($(this).attr('id').slice(-1)), 1);
            }
            // Add new week
            else if (week.length < 3){
                week.push($(this).attr('id').slice(-1));
            }
            // Add sup if there are two of this week
            if (count_items(week, $(this).attr('id').slice(-1)) == 2){
                $(this).children("sup").html("2").css({"padding": "0 4px",
                                                       "border":"1px solid #000",
                                                       "border-radius": "50%"});
            }
            // Add sup if there are three of this week
            else if (count_items(week, $(this).attr('id').slice(-1)) == 3){
                $(this).children("sup").html("3");
            }
            // Delete sup if there is just one this week
            else {
                $(this).children("sup").html("").css({"border": "none"});
            }
            // Clear style if it was deleted from the week list
            if (!week.includes($(this).attr('id').slice(-1))){
                $(this).css({"color":"#000",
                             "font-weight":"normal"});
            }
        }
        // Product list for 4(four) weeks
        else if (num == 4){
            // Add the same week (second of same type)
            if (week.length == 1 && $(this).attr('id').slice(-1) == week[0]){
                week.push($(this).attr('id').slice(-1));
            }
            // Add the same week (third of same type)
            else if (week.length == 2 && $(this).attr('id').slice(-1) == week[0] && $(this).attr('id').slice(-1) == week[1]){
                week.push($(this).attr('id').slice(-1));
            }
            // Add the same week (fourth of same type)
            else if (week.length == 3 && $(this).attr('id').slice(-1) == week[0] && $(this).attr('id').slice(-1) == week[1] && $(this).attr('id').slice(-1) == week[2]){
                week.push($(this).attr('id').slice(-1));
            }
            // Delete week if it was clicked but it is already three of them in the list
            else if (week.length == 4 && week.includes($(this).attr('id').slice(-1))){
                week.splice(week.indexOf($(this).attr('id').slice(-1)), 1);
            }
            // Add new week
            else if (week.length < 4){
                week.push($(this).attr('id').slice(-1));
            }
            // Add sup if there are two of this week
            if (count_items(week, $(this).attr('id').slice(-1)) == 2){
                $(this).children("sup").html("2").css({"padding": "0 4px",
                                                       "border":"1px solid #000",
                                                       "border-radius": "50%"});
            }
            // Add sup if there are three of this week
            else if (count_items(week, $(this).attr('id').slice(-1)) == 3){
                $(this).children("sup").html("3");
            }
            // Add sup if there are four of this week
            else if (count_items(week, $(this).attr('id').slice(-1)) == 4){
                $(this).children("sup").html("4");
            }
            // Delete sup if there is just one this week
            else {
                $(this).children("sup").html("").css({"border": "none"});
            }
            // Clear style if it was deleted from the week list
            if (!week.includes($(this).attr('id').slice(-1))){
                $(this).css({"color":"#000",
                             "font-weight":"normal"});
            }
        }
        // Add week list to the product list data
        prod_list.push(week);
        // Show product list data into the 'check' place
        //$("#check").html(prod_list);
        var data_string = 'data=' + prod_list;
        $.ajax({
            method: "POST",
            url: "/create_list",
            data: data_string,
            cache: false,
            success: function(data){
                var list = "";
                for (let i=0; i<data['num']; i++){
                    list += "<li class='list-group-item d-flex justify-content-between align-items-center'>"+data['prod_name'][i]+
                            "<div><span class='badge badge-primary badge-pill'>"+data['weight'][i].toFixed(2)+"</span>"+
                            "<span class='badge badge-warning badge-pill'>"+data['price'][i].toFixed(2)+"</span></div></li>";
                }
                $(".products-list-2").html("List of products for <b>"+data['weeks']+" week(s)</b>"+
                                        "<ul class='list-group list-group-flush'>"+list+
                                        "<li class='list-group-item d-flex justify-content-between align-items-center' style='font-weight: bold; background-color: rgb(231, 231, 231);'>Total price"+
                                        "<div><span class='badge badge-warning badge-pill'>"+data['total_price'].toFixed(2)+"</span></div></li></ul>");
            }
        });
    });

});