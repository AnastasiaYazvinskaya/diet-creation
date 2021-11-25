/* Menu page (menu.html) */
$(document).ready(function() {
    /* Button to choose the amount of weeks */
    $("section button.week-num").click(function() {
        $(this).css({"color":"#00994d",
                     "font-weight":"bold"});
        var num = $(this).attr('id').slice(-1);
        $("#products_"+num).show();
        for (let k=1; k<5; k++){
            if (k != num){
                $("#list_"+k).css({"color":"#000",
                                  "font-weight":"normal"})
                $("#products_"+k).hide();
            }
        }
    });
    /* Button to choose week to show (list for 1/n week) */
    $("section button.one-week").click(function() {
        $(this).css({"color":"#00994d",
                     "font-weight":"bold"});
        var num = $(this).attr('id').slice(-1);
        $("#one-week_"+num).show();
        for (let k=1; k<5; k++){
            if (k != num){
                $("#list-one-week_"+k).css({"color":"#000",
                                  "font-weight":"normal"})
                $("#one-week_"+k).hide();
            }
        }
    });

    $("section button.two-week-first").click(function() {
        $(this).css({"color":"#00994d",
                     "font-weight":"bold"});
        var num = $(this).attr('id').slice(-1);
        $("#second-week").show();
        for (let k=1; k<5; k++){
            if (k != num){
                $("#list-two-week_"+k).css({"color":"#000",
                                  "font-weight":"normal"})
                $("#second-week_"+k).hide();
            }
        }
    });
});