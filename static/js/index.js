console.log("hii js");
var select = document.getElementById("dropDownData");
var btnGet = document.getElementById("buttonClick");
var myTable = document.getElementById("tableDiv");
let employees = [];
let headers = [];
window.onload = function () {
  var refButton = document.getElementById("btnButton");

  refButton.onclick = function () {
    alert("Dhoor shala!");
  };
};
console.log(select);
// select.addEventListener("onclick", function (e) {
//   var dataType = e.value;
//   var strUser = e.value; // 2
//   var strUser = e.options[e.selectedIndex].text; //test2
//   console.log(dataType, "dataType");
// });

function dropDownData(e) {
  console.log(e, "dropDownData");
  var x = document.getElementById("dropDownData").value;
  console.log(x);
  if (x == 3) {
    document.getElementById(
      "dateAdd"
    ).innerHTML = ` <span class="dataPickerText">MTD</span>
<input class="dataPicker" type="date" id="birthday" name="birthday">`;
    document.getElementById("qYear").innerHTML = "";
  } else if (x == 4) {
    document.getElementById("dateAdd").innerHTML = `  
     <select class="form-select form-select-sm dropDown" aria-label=".form-select-sm example">
    <option selected>Quarter</option>
    <option value="Q-1">Q-1</option>
    <option value="Q-2">Q-2</option>
    <option value="Q-3">Q-3</option>
    <option value="Q-4">Q-4</option>   
</select>
`;
    document.getElementById("qYear").innerHTML = `
<select class="form-select form-select-sm dropDown" aria-label=".form-select-sm example">
<option selected>Year</option>
<option value="2020">2020</option>
<option value="2021">2021</option>
<option value="2022">2022</option>
<option value="2023">2023</option>
<option value="2024">2024</option>
<option value="2025">2025</option>
<option value="2026">2026</option>
</select>
  `;
  } else if (x == 5) {
    document.getElementById("dateAdd").innerHTML = `  
    <select class="form-select form-select-sm dropDown" aria-label=".form-select-sm example">
    <option selected>Year</option>
    <option value="2020">2020</option>
    <option value="2021">2021</option>
    <option value="2022">2022</option>
    <option value="2023">2023</option>
    <option value="2024">2024</option>
    <option value="2025">2025</option>
    <option value="2026">2026</option>
</select>
`;
    document.getElementById("qYear").innerHTML = "";
  } else {
    document.getElementById("dateAdd").innerHTML = "";
    document.getElementById("qYear").innerHTML = "";
  }
  requestCall(x);
}
function requestCall(x) {
  let elements = document.getElementsByName("csrfmiddlewaretoken");
  console.log("hii", elements[0].value);
  $.ajax({
    method: "POST",
    url: "dateFilter/date",
    data: {
      file: "hiii",
      csrfmiddlewaretoken: elements[0].value,
    },
  }).done(function (response) {
    // console.log(response);
    employees = response.data.graph;
    addTable();
  });
}

function addTable() {
  console.log("employees");
  headers = Object.keys(employees[0]);
  document.getElementById("tableDiv").innerHTML = "";

  console.log(employees, "employees");
  let table = document.createElement("table");
  table.className = "aClassName";
  let headerRow = document.createElement("tr");

  headers.forEach((headerText) => {
    let header = document.createElement("th");
    let textNode = document.createTextNode(headerText);
    header.appendChild(textNode);
    headerRow.appendChild(header);
  });

  table.appendChild(headerRow);

  employees.forEach((emp) => {
    let row = document.createElement("tr");

    Object.values(emp).forEach((text) => {
      let cell = document.createElement("td");
      let textNode = document.createTextNode(text);
      cell.appendChild(textNode);
      row.appendChild(cell);
    });

    table.appendChild(row);
  });

  document.getElementById("tableDiv").appendChild(table);
}

// GetCookie
function getCookie(c_name) {
  if (document.cookie.length > 0) {
    c_start = document.cookie.indexOf(c_name + "=");
    if (c_start != -1) {
      c_start = c_start + c_name.length + 1;
      c_end = document.cookie.indexOf(";", c_start);
      if (c_end == -1) c_end = document.cookie.length;
      return unescape(document.cookie.substring(c_start, c_end));
    }
  }
  return "";
}
