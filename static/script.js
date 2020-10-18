ROWS = 30;
COLUMNS = 30;
VISUALIZE_MS = 5;

let mainTbody = $("#main-table");

function clearCells(){
    $("#main-table tr td").removeClass("step-cell")
}
function visualizeCells(data) {
    clearCells();

    timeout = 0;
    
    data["steps"].forEach(cell => {
        timeout += VISUALIZE_MS
        setTimeout(function(){ 
            mainTbody[0].rows[cell[0]].cells[cell[1]].classList.add("step-cell"); 
        }, timeout);
    });

    

}

function calculateAlgorithm() {
    data = getTableInfo();

    // Send board to backend and recieve solution
    $.ajax('/_algorithm?data=' + JSON.stringify(data),
    {
        dataType: 'json', // type of response data
        timeout: 500,     // timeout milliseconds
        success: function (data,status,xhr) {   // success callback function
            visualizeCells(data);
        },
        error: function (jqXhr, textStatus, errorMessage) { // error callback 
            $('p').append('Error: ' + errorMessage);
        }
    });
}

function getTableInfo(){
    // Get table info
    let data = {"start-cell": null,
    "end-cell": null,
    "walls": [],
    "rows": ROWS,
    "columns": COLUMNS};
    $("#main-table tr td").each((index, cell) => {
        let classes = cell.classList;
        let row = Math.floor(index / ROWS);
        let column = index % COLUMNS;
        if (classes.contains("start-cell")){
        data["start-cell"] = [row, column];
        }
        else if (classes.contains("end-cell")){
        data["end-cell"] = [row, column];
        }
        else if (classes.contains("wall-cell")){
        data["walls"].append([row, column]);
        }
    });

    return data
}


// Populate main table with cells
for (let row = 0; row < ROWS; row++){
    let html_string = "<tr>";
    for (let col = 0; col < COLUMNS; col++){
        html_string += "<td></td>";
    }
    html_string += "</tr>";
    mainTbody.append(html_string);
}

// Temporarily set a permanent start and end cell
$("#main-table tr td").first().toggleClass("start-cell")
$("#main-table tr td").last().toggleClass("end-cell")

// Add onClick events
$("button").on("click", calculateAlgorithm);

