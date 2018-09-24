$(document).ready(function(){

    var token = $('#access_token').val();

    alert(token);


    localStorage.setItem('UserToken', $('#access_token').val());
    window.location.href = "/";

});