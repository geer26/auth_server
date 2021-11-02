$(document).ready(function(){
    $('#narrowlogo').hide();
  });


var maincontent = document.getElementById('mc');
var main = document.getElementById('main');
var maxoffset = 400;
var header = document.getElementById('header');
var maxheight = 20;
var minheight = 8;


maincontent.onscroll = function() {

    if (maincontent.scrollTop < maxoffset){
        $('#logoimg').show();
        $('#narrowlogo').hide();
        header.style.height = '20%';

    } else{
        $('#logoimg').hide();
        $('#narrowlogo').show();
        header.style.height = '8%';
    }

}

/*
var image = document.getElementsByClassName('pimage');
new simpleParallax(image, {
    overflow: true,
    scale: 2
});
*/