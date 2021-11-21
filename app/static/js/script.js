/* Menu page (menu.html) */
$(document).ready(function() {
    $("section button").click(function() {
        var num = $(this).attr('id').slice(-1);
        $("#products_"+num).show();
        for (let k=1; k<5; k++){
            if (k != num){
                $("#products_"+k).hide();
            }
        }
    });
});