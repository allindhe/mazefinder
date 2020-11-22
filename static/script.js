let ROWS = 37;  // Must be odd
let COLUMNS = 37;  // Must be odd
let VISUALIZE_MS = 10;

// Keep track on if mouse is down or up and current wall status when clicked
let isMouseDown = false;
let isWallActive = false;

let mainTbody = $("#main-table");

// Start stuff
function clearCells(stepCell=true, wallCell=true){
    if (stepCell){
        $("#main-table tr td").removeClass("step-cell").removeClass("current-step-cell").removeClass("solution-cell")
    }
    if (wallCell){
        $("#main-table tr td").removeClass("wall-cell")
    }
}

function visualizeCells(data) {
    clearCells(stepCell=true, wallCell=false);

    let timeout = 0;
    let previous_cell = null;
    
    // Search
    data["steps"].forEach(cell => {
        timeout += VISUALIZE_MS
        setTimeout(function(){
            // Set class on previous cell
            if (previous_cell){
                previous_cell.classList.remove("current-step-cell");
                previous_cell.classList.add("step-cell");
            }

            // Color current cell
            mainTbody[0].rows[cell[0]].cells[cell[1]].classList.add("current-step-cell");
            previous_cell = mainTbody[0].rows[cell[0]].cells[cell[1]];
        }, timeout);
    });

    // Solution
    previous_cell = null;
    if (data["solution"]){
        data["solution"].forEach(cell => {
            timeout += VISUALIZE_MS
            setTimeout(function(){
                // Set class on previous cell
                mainTbody[0].rows[cell[0]].cells[cell[1]].classList.remove("step-cell");
                mainTbody[0].rows[cell[0]].cells[cell[1]].classList.add("solution-cell");
            }, timeout);
        });
    }
}

function buildMaze(data) {
    clearCells();
    data["walls"].forEach(cell => {
        if (mainTbody[0].rows[cell[0]].cells[cell[1]].classList.length == 0) {
            mainTbody[0].rows[cell[0]].cells[cell[1]].classList.add("wall-cell");
        }
    });
}

function calculateAlgorithm() {
    let inputData = getTableInfo();
    let outputData;

    // Send board to backend and recieve solution
    $.ajax('/_algorithm?data=' + JSON.stringify(inputData) + "&type=" + "Astar",
    {
        dataType: 'json', // type of response data
        timeout: 500,     // timeout milliseconds
        success: function (outputData,status,xhr) {   // success callback function
            visualizeCells(outputData);
        },
        error: function (jqXhr, textStatus, errorMessage) { // error callback 
            console.log('Error: ' + errorMessage);
        }
    });
}
function generateMaze() {
    let inputData = {"rows": ROWS,
                     "columns": COLUMNS};
    let outputData;

    // Send board to backend and recieve solution
    $.ajax('/_maze?data=' + JSON.stringify(inputData) + "&type=" + "Ellers",
    {
        dataType: 'json', // type of response data
        timeout: 500,     // timeout milliseconds
        success: function (outputData,status,xhr) {   // success callback function
            buildMaze(outputData);
        },
        error: function (jqXhr, textStatus, errorMessage) { // error callback 
            console.log('Error: ' + errorMessage);
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
            data["walls"].push([row, column]);
        }
    });

    return data
}

// Do this when DOM is ready
$(function() {

    // Populate main table with cells
    for (let row = 0; row < ROWS; row++){
        let html_string = "<tr>";
        for (let col = 0; col < COLUMNS; col++){
            html_string += "<td id="+(row*COLUMNS+col)+"></td>";
        }
        html_string += "</tr>";
        mainTbody.append(html_string);
    }
    
    // Add onClick for all cells
    $("#main-table td")
        .mousedown(function(){
            isMouseDown = true;
            $(this).toggleClass("wall-cell");
            isWallActive = $(this).hasClass("wall-cell");
            return false; // apperantly prevents text selection
        })
        .mouseover(function(){
            if (isMouseDown){
                $(this).toggleClass("wall-cell", isWallActive)
            }
        });
    // Check if mouse is released
    $(document).mouseup(function () {
        isMouseDown = false;
    });
    
    // Temporarily set a permanent start and end cell
    mainTbody[0].rows[1].cells[0].classList.add("start-cell")
    mainTbody[0].rows[ROWS-2].cells[COLUMNS-1].classList.add("end-cell")
    
    // Add onClick events
    $("#btn-clear").on("click", function() {
        clearCells(stepCell=true, wallCell=false)
    });
    $("#btn-run").on("click", calculateAlgorithm);
    $("#btn-maze").on("click", generateMaze);

})

