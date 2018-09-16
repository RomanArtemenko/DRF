$(document).ready(function(){
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            }
        }
    });


    $.ajax({
        type: "GET",
        url: "http://localhost:8000/api/v1.0/auth/profile/",
//        data: JSON.stringify({'email': $('#inputEmail').val(), "password": $('#inputPassword').val()}),
        contentType: "application/json",
        headers: { 'Authorization': localStorage.getItem('UserToken') },
        cache: false,
        success: function(data){
            console.log(data);
                    alert(data["username"]);
//                    $("#welcome").replace('%username%', data["username"]);
//                    localStorage.setItem('UserToken', data.split(':')[1]);
//            localStorage.setItem('UserToken', data);
//            window.location.href = "http://localhost:8000";
//            document.cookie = "Authorization=" + data;
//                    alert( document.cookie );

        },
        error: function(xhr){

            console.log(xhr);
        }
    });

});