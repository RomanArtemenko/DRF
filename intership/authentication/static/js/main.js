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
        url: "/api/v1.0/auth/profile/",
        contentType: "application/json",
        headers: { 'Authorization': localStorage.getItem('UserToken') },
        cache: false,
        success: function(data){
            var el_p = $('#welcome').find('p');
            el_p.text(el_p.text().replace('%username%', data["username"]));
        },
        error: function(xhr){
            console.log(xhr);
        }
    });

});