
var visible_tab = 'users';


$(document).ready(function(){
    $('.fixed-action-btn').floatingActionButton();
    //more to init
    visible_tab = 'users';
    //hide_all_details();
  });


function get_admindata(){
    show_loader();
    $.ajax({
            url: '/API/admindata_html',
            type: 'GET',

            success: result => {
                //console.log(result);
                hide_loader();
                //window.location.href = "/";
                $('#main').empty();
                $('#main').append(result['html']);
                $("[data-target="+visible_tab.toString()+"]").click();
                get_logs();
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                console.log(jqXhr);
            }
    });
}


function change_enable(id){
    show_loader();
    $.ajax({
            url: '/API/change_enable',
            type: 'POST',
            dataType: "json",
            data: JSON.stringify({id: id}),
            contentType: "application/json; charset=utf-8",

            success: result => {
                //console.log(result);
                hide_loader();
                //window.location.href = "/";
                $('#main').empty();
                $('#main').append(result['html']);
                $("[data-target="+visible_tab.toString()+"]").click();
                get_logs();
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                console.log(jqXhr);
            }
    });
}


function hide_all_tabs(){
    $('.adm').removeClass('admin_chunk-active');
    $('.adm').addClass('admin_chunk-hidden')
    $('.men').removeClass('menuitem-active');
    $('.men').addClass('menuitem');
}


function show_tab(elem){
    hide_all_tabs();
    $(elem).removeClass('menuitem');
    $(elem).addClass('menuitem-active');
    var target = elem.getAttribute('data-target');
    $('#'+target.toString()).addClass('admin_chunk-active');
    visible_tab = target;
}


function hide_all_details(){
    $('.user-detail').addClass('user-detail-hidden');
    $('.user-detail').addClass('user-detail-ready-to-close');
}


function show_user_details(id, target){
    hide_all_details();

    if ($(target).hasClass('user-detail-ready-to-close')){
        $(target).removeClass('user-detail-ready-to-close');
        return;
    }

    $(target).addClass('user-detail-ready-to-close');
    var u = "user-" + id.toString();
    $('#'+u).removeClass('user-detail-hidden');
}


function hide_error(){
    $('.error').hide();
}


function show_chpw(id){
    $('#chpw_back').show();
    $('#chpw_back').data('id', id);
}


function change_password(id){
    //get and validate data!!!
    var pw1 = $('#password1').val();
    var pw2 = $('#password2').val();
    //check match
    if (pw1 != pw2){
        //show error message
        $('.error').text("A két jelszó nem egyezik!");
        $('.error').show();
        return;
    }
    var data_to_post = JSON.stringify( {id: id, pw: pw1} );
    show_loader();
    $.ajax({
            url: '/API/change_password',
            type: 'POST',
            dataType: "json",
            data: data_to_post,
            contentType: "application/json; charset=utf-8",

            success: result => {
                $('#chpw_back').hide();
                hide_loader();
                //$('#main').empty();
                //$('#main').append(result['html']);
                //$("[data-target="+visible_tab.toString()+"]").click();
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                console.log(jqXhr);
            }
    });
}


function show_adduser_modal(){
    $('#adduser_username').val('');
    $('#adduser_pw1').val('');
    $('#adduser_pw2').val('');
    $('#adduser_email').val('');
    $('#adduser_error').hide();
    $('#adduser_back').show('');
}


function add_user(){
    //get data
    var uname = $('#adduser_username').val();
    var pw1 = $('#adduser_pw1').val();
    var pw2 = $('#adduser_pw2').val();
    var email = $('#adduser_email').val();
    var is_enabled = $('#adduser_isactive').prop('checked');
    var is_superuser = $('#adduser_issuperuser').prop('checked');

    //validate inputs
    if (uname == '' || pw1 == '' || pw2 == '' || email == ''){
        $('#adduser_error').text("Hiányos kitöltés!");
        $('#adduser_error').show();
        return;
    }

    if(pw1 != pw2){
        $('#adduser_error').text("A két jelszó nem egyezik!");
        $('#adduser_error').show();
        return;
    }

    var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    if (!re.test(String(email).toLowerCase())){
        $('#adduser_error').text("Érvénytelen email cím!");
        $('#adduser_error').show();
        return;
    }

    var data_to_post = JSON.stringify({username: uname, password: pw1, email: email, is_enabled: is_enabled, is_superuser: is_superuser});

    //console.log(data_to_post);
    show_loader();

    $.ajax({
            url: '/API/adduser_htm',
            type: 'POST',
            dataType: "json",
            data: data_to_post,
            contentType: "application/json; charset=utf-8",

            success: result => {
                $('#adduser_back').hide();
                hide_loader();
                $('#main').empty();
                $('#main').append(result['html']);
                $("[data-target="+visible_tab.toString()+"]").click();
                get_logs();
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                $('#adduser_error').text("Sikertelen művelet!");
                $('#adduser_error').show();
                console.log(jqXhr);
            }
    });

}


function delete_user(id){
    console.log('DELETE USER: ', id);
    var id = id;
    if (!id){return;}
    var data_to_post = JSON.stringify( {uid: id} );
    show_loader();
    $.ajax({
            url: '/API/deluser_htm',
            type: 'POST',
            dataType: "json",
            data: data_to_post,
            contentType: "application/json; charset=utf-8",

            success: result => {
                hide_loader();
                $('#main').empty();
                $('#main').append(result['html']);
                $("[data-target="+visible_tab.toString()+"]").click();
                get_logs();
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                $('#adduser_error').text("Sikertelen művelet!");
                $('#adduser_error').show();
                console.log(jqXhr);
            }
    });
    return;
}


function get_logs(){
    show_loader();

    $.ajax({
            url: '/API/getlog_ashtml',
            type: 'GET',

            success: result => {
                hide_loader();
                $('#log_viewer').empty();
                $('#log_viewer').append(result['html']);
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                $('#adduser_error').text("Sikertelen művelet!");
                $('#adduser_error').show();
                console.log(jqXhr);
            }
    });
}


function change_key(){
    show_loader();

    $.ajax({
            url: '/API/changekey',
            type: 'GET',

            success: result => {
                get_admindata();
            },

            error: (jqXhr, textStatus, errorMessage) => {
                hide_loader();
                $('#adduser_error').text("Sikertelen művelet!");
                $('#adduser_error').show();
                console.log(jqXhr);
            }
    });
}


function download_current_log(){
    location.href = '/get_current_log';
    return;
}


function download_archive_log(){
    location.href = '/get_archive_log';
    return;
}