function changePlayer(index,selectObject){
    let player_id = selectObject.value;
    document.getElementById(`goals_${index}`).setAttribute("name",`goals_${player_id}`);
    let url = `/api/player_image_url/${player_id}`
    $.getJSON(url, function(data) {
        let image = document.getElementById(`image_${index}`)
        image.src = data;
    });
}

function playerInputs(ele){
    let numberOfPlayers = ele.value;
    let generalPlayerInput = document.getElementById("player_input");
    let container = document.getElementById("player_inputs_container");
    container.innerHTML = "";
    for (let i = 0; i < numberOfPlayers; i++) {
        let playerInput = generalPlayerInput.cloneNode('deep')
        playerInput.style.display = "block";
        let select = playerInput.getElementsByTagName("select")[0];
        let label = playerInput.getElementsByTagName("label")[0];
        select.setAttribute("name",`player_${i}`);
        select.setAttribute("id",`player_${i}`);
        label.setAttribute("for",`player_${i}`);
        container.appendChild(playerInput);
    }
}