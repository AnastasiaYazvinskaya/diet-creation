open = 0
function selectAvatar() {
    if (open == 0){
        data = "data="+open;
        $.ajax({
            method: "POST",
            url: "/choose_avatar",
            data: data,
            cache: false,
            success: function(data){
                var list = '<div id="choose-avatar">';
                $('.test').html(data['id'][0]);
                for (let i=0; i<data['id'].length; i++){
                    list += '<div><img src ="'+data['icon'][i]+'" alt = "Alternate user icon" onclick="changeIcon('+data['id'][i]+')"></div>';
                }
                list += '</div>';
                $(".choose-avatar").html(list);
            }
        });
        open++;
    }
    else {
        $(".choose-avatar").html('');
        open--;
    }
}
function changeIcon(icon) {
    var data_string = 'data='+icon;
    $.ajax({
        method: "POST",
        url: "/update_icon",
        data: data_string,
        cache: false,
        success: function(data){
            $("div.navbar-brand").html("<img src ='"+data['icon']+"' alt = 'User icon'/>");
        }
    });
}