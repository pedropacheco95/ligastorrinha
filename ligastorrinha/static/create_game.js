function changePlayer(index,selectObject){
    console.log(selectObject)
    let player_id = selectObject.value;
    document.getElementById(`goals_${index}`).setAttribute("name",`goals_${player_id}`);
    let url = `/api/player_image_url/${player_id}`
    $.getJSON(url, function(data) {
        let image = document.getElementById(`image_${index}`)
        console.log(image)
        image.src = data;
    });
}