function openHint() {
    var hint = document.getElementById("hint");
    //toggle adds a class if it's not there or removes it if it is.
    hint.classList.toggle("open-hint");
}
function recipes(type, user) {
    var data = 'data='+type;
    if (type != 0){
        $(".recipes-header #my").css("font-weight", "700");
        $(".recipes-header #total").css("font-weight", "400");
    }
    else {
        $(".recipes-header #my").css("font-weight", "400");
        $(".recipes-header #total").css("font-weight", "700");
    }
    $.ajax({
        method: "POST",
        url: "/recipes_list",
        data: data,
        cache: false,
        success: function(data){
            var list = "";
            if (data['id'].length != 0) {
                for (let i=0; i<data['id'].length; i++){
                    let url = Flask.url_for('recipe', {'recipe_id': data['id'][i]});
                    if (user != data['created_by'][i]){
                        list += "<div class='recipe-info'>";
                    }
                    else {
                        list += "<div class='recipe-info my-recipe'>";   
                    }
                    list += "<a href='"+url+"'><h4>"+data['name'][i]+"</h4><div class='recipe-type'>";
                            if (data['type'][i] != 'general'){
                                list += data['type'][i]+"</div><p>Ингредиенты: "+data['ingreds'][i]+"</p></a>";
                            }
                            else {
                                list += "<br></div><p>Ингредиенты: "+data['ingreds'][i]+"</p></a>";
                            }
                            
                    if (user != data['created_by'][i]){
                        style = "";
                        if (data['heart'][i]){
                            style = "style='color: red;'";
                        }
                        list += "<div id='recipe_"+data['id'][i]+"' class='heart' onclick='like(1, "+user+", "+data['id'][i]+")' "+style+">&#9829;</div></div>";
                    }
                    else {
                        list += '<div class="acts"><form action="'+Flask.url_for('delete_r', {'recipe_id':data['id'][i]})+'" method="POST">'+
                        '<input type="image" src="../static/images/delete2.svg" value="Удалить" id="delete"'+
                        '        onclick="return confirm("Подтвердите удаление")">'+
                        '</form><a href="'+Flask.url_for('edit_r', {'recipe_id': data['id'][i]})+'">'+
                        '<img src="../static/images/edit.svg" alt="Edit icon">'+
                        '</a></div></div>';   
                    }
                            
                }
            }
            else {
                if (type == 0){
                    list += "<div class='recipe-info'><p style='text-align: center;'>Пока что в нашей базе нет ни одного рецепта</p></div>";
                }
                else {
                    list += "<div class='recipe-info'><p style='text-align: center;'>Пока что вы не добавили ни одного рецепта</p>"+
                            "<a href='"+Flask.url_for('create_r')+"'><span class='add-btn badge badge-primary'>Добавить рецепт</span></a></div>";   
                }
            }
            $("#list-of-recipes").html(list);
        }
    }); 
}
function like(i=0, user, recipe) {
    data = "like="+[i, user, recipe];
    $.ajax({
        method: "POST",
        url: "/like",
        data: data,
        cache: false,
        success: function(data){
            if (data['like'] == 0) {
                $('#recipe_'+recipe).css("color", "rgba(61, 61, 61, 0.2)");
            }
            else {
                $('#recipe_'+recipe).css("color", "red");
            }
        }
    });
}