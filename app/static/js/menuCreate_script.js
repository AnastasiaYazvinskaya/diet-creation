var week = 2;

$(document).ready(function() {
    /* Menu Creation */

    /* Additional place for recipes (accessiable 4 additional places)*/
    $(".addItem button").click(function(event) {
        type_id = $(this).closest("tr").attr("id"); //meal_n
        week_id = $(this).closest(".week").attr("id"); //week_n
        item = parseInt($(this).children("div").text());
        
        $("#"+week_id+" ."+type_id+"-place_"+item).show();
        $(this).children("div").html(item+1);
        if (item > 3) {
            $(this).closest("tr").hide();
        }
        
        $("#check").html("Item "+ item +" was Added")
    });
    /* Add new week (accessiable 4 weeks) */
    $("#addWeek").click(function(event) {
        $("#week_"+week).show();
        // Changing index
        week += 1;
        // Hide adding button if 30 ingredients was added
        if (week > 4) {
            $(this).hide();
        }

        $("#check").html("Week was Added")
    });

    /* Show and hide recipes according to the clicked button */
    for (let j=0; j<10; j++){
        //let sel1 = "#show_"+j;
        //let sel2 = "#"+j+"_hide";
        $("#show_"+j).click(function(event){
            $("#"+j+"_hide").show();
            for (let k=0; k<10; k++){
                //let sel3 = "#"+k+"_hide";
                if (k != j){
                    $("#"+k+"_hide").hide();
                }
            }
        });
    }
    /* Create draggable objects */
    $(".drag").draggable({
        containment: "#menu-container",
        helper: "clone",
        revert: "invalid"
    });

    var data2 = new Array();
    data2.push($(".create-edit").attr("id"));
    $('.drop-meal_1').droppable({
        accept: ".meal_1",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.text())
                .css("background-color", "rgba(95, 255, 80, 0.521)");

            var data1 = new Array(5);
            data1[0] = ui.draggable.text();
            data1[1] = $(this).parent().attr("id").slice(-1);
            data1[2] = $(this).closest(".week").attr('id').slice(-1);
            data1[3] = 1; //Breakfast
            data1[4] = $(this).attr("id").slice(-1);
            data2.push(data1);
        }
    });
    $('.drop-meal_2').droppable({
        accept: ".meal_2",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.text())
                .css("background-color", "rgba(95, 255, 80, 0.521)");

            var data1 = new Array(5);
            data1[0] = ui.draggable.text();
            data1[1] = $(this).parent().attr("id").slice(-1);
            data1[2] = $(this).closest(".week").attr('id').slice(-1);
            data1[3] = 2; //Lunch
            data1[4] = $(this).attr("id").slice(-1);
            data2.push(data1);
        }
    });
    $('.drop-meal_3').droppable({
        accept: ".meal_3",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.text())
                .css("background-color", "rgba(95, 255, 80, 0.521)");

            var data1 = new Array(5);
            data1[0] = ui.draggable.text();
            data1[1] = $(this).parent().attr("id").slice(-1);
            data1[2] = $(this).closest(".week").attr('id').slice(-1);
            data1[3] = 3; //Dinner
            data1[4] = $(this).attr("id").slice(-1);
            data2.push(data1);
        }
    });
    $('.drop-meal_4').droppable({
        accept: ".meal_4",
        drop: function( event, ui ) {
            $( this )
                .html(ui.draggable.text())
                .css("background-color", "rgba(198, 253, 193, 0.521)");
            
            var data1 = new Array(5);
            data1[0] = ui.draggable.text();
            data1[1] = $(this).parent().attr("id").slice(-1);
            data1[2] = $(this).closest(".week").attr('id').slice(-1);
            data1[3] = $(this).attr("id").slice(5, 6);
            data1[4] = $(this).attr("id").slice(-1);
            data2.push(data1);
        }
    });

    $("#send").click(function(event) {
        if ($('#menu_name').val() != ""){
            data2.unshift($('#menu_name').val());
        }
        if ($("#menu_id").attr("id")) {
            data2.unshift($("#menu_id").text());
        }
        var data_string = 'data='+data2;
        $.ajax({
            method: "POST",
            url: "/update_menu",
            data: data_string,
            cache: false,
            success: function(data){
                window.location.href = data;
            }
        });
    });
});