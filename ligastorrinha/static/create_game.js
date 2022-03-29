function changePlayer(index,selectObject){
    let player_id = selectObject.value;
    document.getElementById(`goals_${index}`).setAttribute("name",`goals_${player_id}`);
}