$(document).ready(function(){
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
                xhr.setRequestHeader("RRRRRRRRRRRRRRRR", 'XA XA xa ');
            }
        }
    });

    $('#buttonSignIn').on('click', function(){
        if ($('#inputEmail').val() && $('#inputPassword').val()) {
            $.ajax ({   url : "http://localhost:8000/profile/",
            headers: { 'XXX Authorizationn' : 'sasaaadad' });

            $.ajax({
                type: "POST",
                url: "http://localhost:8000/api/v1.0/auth/signin/",
                data: JSON.stringify({'email': $('#inputEmail').val(), "password": $('#inputPassword').val()}),
                contentType: "application/json",
                cache: false,
                success: function(data){
                    console.log(data);
//                    alert(data);
//                    localStorage.setItem('UserToken', data.split(':')[1]);
                    localStorage.setItem('UserToken', data);
//                    window.location.href = "http://localhost:8000";
                    document.cookie = "Authorization=" + data;



//                    alert( document.cookie );

                },
                error: function(xhr){

                    console.log(xhr);
                }
            });
        }
    });

    $('#buttonRegister').on('click', function(){
        if ($('#inputEmail').val() && $('#inputPassword').val() && $('#inputPasswordConfirm').val() && $('#inputUserName').val() && $('#inputFirstName').val() && $('#inputLastName').val()) {
            $.ajax({
                type: "POST",
                url: "http://localhost:8000/api/v1.0/auth/signup/",
                data: JSON.stringify({
                    'email': $('#inputEmail').val(),
                    'username': $('#inputUserName').val(),
                    'first_name': $('#inputFirstName').val(),
                    'last_name': $('#inputLastName').val(),
                    "password": $('#inputPassword').val(),
                    "confirm_password": $('#inputPasswordConfirm').val()
                 }),
                contentType: "application/json",
                cache: false,
                success: function(data){
                    console.log(data);
                    window.location.href = "http://localhost:8000/login"
//                    alert(data);
//                    localStorage.setItem('UserToken', data.split(':')[1]);
                },
                error: function(xhr){

                    console.log(xhr);
                }
            });
        }
    });

});