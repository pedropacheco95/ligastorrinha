function redirect(url){
    $.ajax({
        url: url,
        method: "GET",
        success: call_back()
    })
}

/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            var i;
            for (i = 0; i < dropdowns.length; i++) {
                    var openDropdown = dropdowns[i];
                    if (openDropdown.classList.contains('show')) {
                            openDropdown.classList.remove('show');
                    }
            }
    }
}

function ShowPlayerInputs(){
    let divs = document.getElementsByClassName('optional');
    for (let div of divs){
        div.style.display = 'block'
    }
}