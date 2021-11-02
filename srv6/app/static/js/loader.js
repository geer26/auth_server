function show_loader(){
    var loader = document.getElementById('loader_back');
    loader.classList.remove("hidden-loader");
    loader.classList.add('visible-loader');
}

function hide_loader(){
    var loader = document.getElementById('loader_back');
    loader.classList.remove("visible-loader");
    loader.classList.add('hidden-loader');
}