function toggleNav(elem){
    var liArray=document.getElementById("nav_ul").childNodes;
    var i = 0;
    while(liArray[i]){
        liArray[i].id = "";
        i++;
    }
    elem.id="current";     
}

function setContent(id, path){
    var cid = id;
    $.get(path, function(data){
        $("#"+cid).html(data);
    });  
}