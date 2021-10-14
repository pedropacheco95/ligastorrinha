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
    for (let optional of optionals){
        optional.style.display = 'none';
    }
    for (let not_optional of not_optionals){
        not_optional.innerHTML = not_optional.getAttribute("name")[0];
    }
    let special_column = document.getElementsByName('Golos/Presença')[0];
    special_column.innerHTML = 'G/P'
}

function enlargeWindow(){
    let optionals = document.getElementsByClassName('optional');
    let not_optionals = document.getElementsByClassName('not_optional');
    for (let optional of optionals){
        optional.style.display = '';
    }
    for (let not_optional of not_optionals){
        not_optional.innerHTML = not_optional.getAttribute("name");
    }
}