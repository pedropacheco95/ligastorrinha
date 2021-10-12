window.addEventListener('load',function(){
    if (window.innerWidth < 850){
        reduceWindow();
    };
    if (window.innerWidth > 850){
        enlargeWindow();
    };
})

window.addEventListener('resize',function(){
    if (window.innerWidth < 850){
        reduceWindow();
    };
    if (window.innerWidth > 850){
        enlargeWindow();
    };
})

function reduceWindow(){
    let frames = document.getElementsByClassName('videos');
    for (let frame of frames){
        frame.width = '250';
        frame.height = '200';
    }
}

function enlargeWindow(){
    let frames = document.getElementsByClassName('videos');
    for (let frame of frames){
        frame.width = '800';
        frame.height = '440';
    }
}