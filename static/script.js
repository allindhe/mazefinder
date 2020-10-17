ROWS = 10;
COLUMNS = 10;

let mainTable = $("#main-table");

// Populate main table with cells
for (let row = 0; row < ROWS; row++){
    let html_string = "<tr>";
    for (let col = 0; col < COLUMNS; col++){
        html_string += "<td></td>";
    }
    html_string += "</tr>";
    mainTable.append(html_string);
}