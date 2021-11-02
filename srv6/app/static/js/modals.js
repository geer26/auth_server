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

    var data = {username: $('#username').val(), password: $('#password').val(), remember_me: $('#remember_me').prop('checked')};

    show_loader();

    $.ajax({
            url: '/API/login',
            data: data,
            type: 'GET',

            success: result => {
                console.log(result);
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