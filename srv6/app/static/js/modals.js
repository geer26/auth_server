function hide_all(){
    $('.modalback').hide();
}


function show_login(){
    hide_all();
    $('[data-target="loginmodal"]').show();
}


function hide_error(){
    $('#errormessage').hide();
}


function press_login(){

    if ($('#username').val() == '' || $('#password').val() == ''){
        $('#errormessage').text("Minden mező kitöltése kötelező!");
        $('#errormessage').show();
        return;
    }

    var data = {username: $('#username').val(), password: $('#password').val(), remember: $('#remember_me').prop('checked')};

    show_loader();

    $.ajax({
            url: '/API/login',
            type: 'POST',
            dataType: "json",
            data: JSON.stringify(data),
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                window.location.href = "/";
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                $('#errormessage').text(jqXhr.responseJSON['message']);
                $('#errormessage').show();
            }
    });

}