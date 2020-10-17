ROWS = 10;
COLUMNS = 10;
NCELLS = ROWS * COLUMNS;

let mainTbody = $("#main-table");

// Populate main table with cells
for (let row = 0; row < ROWS; row++){
    let html_string = "<tr>";
    for (let col = 0; col < COLUMNS; col++){
        html_string += "<td></td>";
    }
    html_string += "</tr>";
    mainTbody.append(html_string);
}

// Temporarily set a permanent start and end
$("#main-table tr td").first().toggleClass("start-cell")
$("#main-table tr td").last().toggleClass("end-cell")

// Get table info
let data = {"start-cell": null,
            "end-cell": null,
            "walls": [],
            "rows": ROWS,
            "columns": COLUMNS};
$("#main-table tr td").each((index, cell) => {
    let classes = cell.classList;
    if (classes.contains("start-cell")){
        data["start-cell"] = [Math.floor(index / ROWS), index % COLUMNS]
    }
    else if (classes.contains("end-cell")){
        data["end-cell"] = [Math.floor(index / ROWS), index % COLUMNS]
    }
});
console.log(data)