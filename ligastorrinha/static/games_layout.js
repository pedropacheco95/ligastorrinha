window.addEventListener('load',function(){
    if (window.innerWidth < 775){
        reduceWindow();
    };
    if (window.innerWidth > 775){
        enlargeWindow();
    };
})

window.addEventListener('resize',function(){
    if (window.innerWidth < 775){
        reduceWindow();
    };
    if (window.innerWidth > 775){
        enlargeWindow();
    };
})

function reduceWindow(){
    let optionals = document.getElementsByClassName('optional');
    let not_optionals = document.getElementsByClassName('not_optional');
    let game_info_container = document.getElementsByClassName('game_info_container')[0];
    game_info_container.style.width = '100%';
    for (let optional of optionals){
        optional.style.display = 'none';
    }
    for (let not_optional of not_optionals){
        not_optional.innerHTML = not_optional.getAttribute("name")[0];
    }
}

function enlargeWindow(){
    let optionals = document.getElementsByClassName('optional');
    let not_optionals = document.getElementsByClassName('not_optional');
    let game_info_container = document.getElementsByClassName('game_info_container')[0];
    game_info_container.style.width = '70%';
    for (let optional of optionals){
        optional.style.display = '';
    }
    for (let not_optional of not_optionals){
        not_optional.innerHTML = not_optional.getAttribute("name");
    }
}