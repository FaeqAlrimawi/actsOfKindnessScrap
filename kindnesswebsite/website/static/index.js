
var global_row = -1;
var global_act = "";
// var initialized = false;
var gridOptions;

function delete_AoK(aokId){
    fetch('/delete-AoK', {
        method: 'POST',
        body: JSON.stringify({aokId: aokId})
    }).then((_res) => {
        window.location.href="/edit";
    });
}

function getSelectedRows() {
  var selectedNodes = gridOptions.api.getSelectedNodes()
  var selectedData = selectedNodes.map( function(node) { return node.data })
  var selectedDataStringPresentation = selectedData.map( function(node) { return node.text + ' ' + node.prob_aok }).join(', ')
  alert('Selected nodes: ' + selectedDataStringPresentation);
}


function headerHeightSetter() {
  var padding = 20;
  var height = headerHeightGetter() + padding;
  gridOptions.api.setHeaderHeight(height);
}

function headerHeightGetter() {
  var columnHeaderTexts = [
      ...document.querySelectorAll('.ag-header-cell-text'),
  ];
  var clientHeights = columnHeaderTexts.map(
      headerText => headerText.clientHeight
  );
  var tallestHeaderTextHeight = Math.max(...clientHeights);

  return tallestHeaderTextHeight;
}

function createActsGrid() {
  // Grid Options are properties passed to the grid
   gridOptions = {

    // each entry here represents one column
    columnDefs: [
      { field: "id", hide:true }, //checkboxSelection: true
      { field: "text",  editable: true, minWidth: 500, checkboxSelection: true},
      { field: "prob_aok", maxWidth: 120},      
    ],

    

    onFirstDataRendered: headerHeightSetter,
    onColumnResized: headerHeightSetter,

    onGridSizeChanged: () => {
      gridOptions.api.sizeColumnsToFit();
  } ,    

    // default col def properties get applied to all columns
    defaultColDef: {sortable: true, filter: true,  wrapText: true,  
    autoHeight: true, resizable: true},
    
    // enableRangeSelection: true,
    // fillHandleDirection: 'x',
    // enableFillHandle: true,
    
    rowSelection: 'multiple', // allow rows to be selected
    animateRows: true, // have rows animate to new positions when sorted

    pagination: true,
    paginationAutoPageSize: true,
    // example event handler
    // onCellClicked: params => {
    //   console.log('cell was clicked', params)
    // }
  };

  // get div to host the grid
  const eGridDiv = document.getElementById("myGrid");
  // new grid instance, passing in the hosting DIV and Grid Options
  new agGrid.Grid(eGridDiv, gridOptions);

  // Fetch data from server
  fetch("/api/actdata")
  .then(response => response.json())
  .then(data => {
    // load fetched data into grid
    // console.log(data[0]);
    gridOptions.api.setRowData(data);
  });
}


function add_Aoks() {

  const selectedNodes = gridOptions.api.getSelectedNodes();

    //label
    var lbl = document.getElementById("lbl-add");
    lbl.innerHTML = "";
  
    
  if (selectedNodes.length == 0 ) {
    lbl.innerHTML = "<span style='color: red;'>"+
    "Please select acts from the table to add";
    return;
  }

  var selectedData = selectedNodes.map( function(node) { return node.data });

  var mapResult = new Map();



  for(let i=0;i<selectedData.length;i++) {
    actID = selectedData[i].id;

    message = add_AoK(actID);

    if (message == "error"){
      mapResult.set(actID, message);
    } else {
      //delet from table
      
    }
    
  }

  if(mapResult.size == 0) {
    lbl.innerHTML = "<span style='color: green;'>"+
    "Successfully added <b>"+ selectedData.length+"</b> act(s)</span>";
    gridOptions.api.applyTransaction({remove: selectedNodes});
  } else {
    lbl.innerHTML = "<span style='color: red;'>"+
    "Could not add "+ mapResult.length+" acts</span>";
  }
//   // deal with results
//   if(message == 'exists') {
//     // console.log('act already exists in the database');
//     // span.html = '&#79;'; 
//     //  btn.css("cursor", "default");
//     //  btn.attr("onclick", "").unbind("click");
//     //  btn.attr("title", "Already exists");
     
// } else if (message == 'added'){
//     // span.html = '&#10004;'; 
//     // btn.css("cursor", "default");
//     // btn.attr("onclick", "").unbind("click");
//     // btn.attr("title", "Added successfully");
//     console.log("act added succefsuly");

// } else if (message == 'error') {
//   //  console.log('error adding the act');     
// }

 

}

function add_AoK(actID){

  //  if (btn) {
  //   span = btn.childNodes[0]
  //  }

   // var act = $('#td-'+row).text();
    // console.log("row: "+row +" act: " + act);
    
    fetch('/add-AoK', {
        method: 'POST',
        body: JSON.stringify({actID: actID}),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => {

        return response.json();        
    }).then((data) => {
        
        message = data['message'];

       return message; 
    }

    ).catch(err => console.log(err));
}

// function updateAoKText(row, old_act){

//     var act = $('#txtarea-'+row).val();

//     //alert(act);
//     $('#td-'+row).html(act);
   
//    $('#td-'+row).bind("click", function (){ update_AoK('+row+'); }); 

//    global_act = act;

//    //update add button if needed
//    btnRow = $('#btn-'+row);

//    if(act !== old_act) {
//     let btnSpan = btnRow.find('span');
//     // let spanValue = btnSpan.text();
    
//      //if already added
//     // if(spanValue === '&#10004;'){
//         btnSpan.html('&plus;'); 
//         btnRow.css("cursor", "pointer");
//         btnRow.attr("onclick", "").unbind("click");
//         btnRow.bind("click", function (){ add_AoK(row); });
        
//     // } 
//     fetch('/update-prob', {
//         method: 'POST',
//         body: JSON.stringify({aok: act}),
//         cache: "no-cache",
//         headers: new Headers({
//             "content-type": "application/json"
//         })
//     }).then((response) => {
//         return response.json();
//    }).then((data) => {
//         prob = data['prob'];
//         // console.log("ooooo "+prob);
//         var rounded = Math.round(prob * 100) / 100;
//         $('#td-prob-'+row).html(rounded);
       
//    });

// }

   
// }


// function cancelAoKUpdate(act, row){

   
//     $('#td-'+row).html(act);

    
//     $('#td-'+row).bind("click", function (){ update_AoK('+row+'); });

    
// }

// function cancelAoKUpdateESC(e, act, row){

//     e = e || window.event;
//     var code = e.keyCode;

//     if(code == 27) {
//         cancelAoKUpdate(act, row);
//     }

 

// }

// function update_AoK(row){

//     var act = $('#td-'+row).text().trim();

//     if(global_row != -1) {
//         $('#td-'+global_row).html(global_act);
        
//         $('#td-'+global_row).attr("onclick", 'update_AoK('+global_row+')').bind("click");
        
//     }


//         $('#td-'+row).html('<div align="left" style="width:100%;"> ' +
//             '<textarea  name="act"  id="txtarea-'+row+ '" onKeyDown="cancelAoKUpdateESC(event, \''+act+'\',' + row +')" style="width:100%">'+act+'</textarea>' +
            
//             '<button type="button"  class="btn btn-secondary" onClick="updateAoKText('+ row + ',\''+act+'\'' + ')">Update</button>' +

//             '&nbsp;&nbsp;' +
            
//             '<button type="button"  class="btn btn-secondary" onClick="cancelAoKUpdate(\''+act+'\',' + row +')">Cancel</button>' +
            
//             '</div>');
        
//         $('#td-'+row).attr("onclick", "").unbind("click");

//         $('#txtarea-'+row).focus();
        
//         global_row = row;
//         global_act = act;
   
// }


function checkURL (abc) {
    var string = abc.value;
    if (!~string.indexOf("http")) {
      string = "http://" + string;
    }
    abc.value = string;
    return abc
  }


function getContactFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}


function scrap(websiteURL) {

    // console.log("@@@ " + websiteURL);
    $('#websiteURL').val(websiteURL);
 
    $('#scrapForm').trigger('submit');
}

function getContactFormData(form) {
  // creates a FormData object and adds chips text
  var formData = new FormData(document.getElementById(form));
//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
  return formData
}


function scrap(websiteURL) {

  // console.log("@@@ " + websiteURL);
  $('#websiteURL').val(websiteURL);

  $('#scrapForm').trigger('submit');
}



function createGridjsTable(tableID, serverURL, columnsDetails) {

  const tableDiv = document.getElementById(tableID);

  const updateUrl = (prev, query) => {
    return prev + (prev.indexOf('?') >= 0 ? '&' : '?') + new URLSearchParams(query).toString();
  };
  
  new gridjs.Grid({
    columns:columnsDetails,
    server: {
      url: serverURL,
      then: results => results.data,
      total: results => results.total,
    },
    search: {
      enabled: true,
      server: {
        url: (prev, search) => {
          return updateUrl(prev, {search});
        },
      },
    },
    sort: {
      enabled: true,
      multiColumn: true,
      server: {
        url: (prev, columns) => {

          let columnIds = [];//['id', 'act', 'source', 'date'];

         for(let i=0;i<columnsDetails.length;i++) {
           columnIds.push(columnsDetails[i]['id']);
          }
          // console.log("col: "+columnIds);
          const sort = columns.map(col => (col.direction === 1 ? '+' : '-') + columnIds[col.index]);
          return updateUrl(prev, {sort});
        },
      },
    },
    pagination: {
      enabled: true,
      server: {
        url: (prev, page, limit) => {
          return updateUrl(prev, {start: page * limit, length: limit});
        },
      },
    },
  }).render(tableDiv);

  let savedValue;

  tableDiv.addEventListener('focusin', ev => {
    if (ev.target.tagName === 'TD') {
      savedValue = ev.target.textContent;
    }
  });

  tableDiv.addEventListener('focusout', ev => {
    if (ev.target.tagName === 'TD') {
      if (savedValue !== ev.target.textContent) {
        fetch(serverURL, {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            id: ev.target.dataset.elementId,
            [ev.target.dataset.columnId]: ev.target.textContent
          }),
        });
      }
      savedValue = undefined;
    }
  });

  tableDiv.addEventListener('keydown', ev => {
    if (ev.target.tagName === 'TD') {
      if (ev.key === 'Escape') {
        ev.target.textContent = savedValue;
        ev.target.blur();
      }
      else if (ev.key === 'Enter') {
        ev.preventDefault();
        ev.target.blur();
      }
    }
  });

}




// function scrapAoKs(){
//     var url = $("#websiteURL").val();
//     console.log("### " + url);
//     fetch('/aok-scrapper', {
//         method: 'POST',
//         body: JSON.stringify({websiteURL: url})
//     }).then((response) => {
//         return response.json();
//     }).then((data)=> {
//         res = data['result'];
//         console.log(res);
//         acts = JSON.parse(data.acts);
//         // console.log(acts[0]['act']);
        
//         table = $('#aoks');
//         // rowIndex = 0;
//         $('#aoks > tbody').empty();
//         acts.forEach(function(element)  {
//             table.append('<tr>' +
//             '<td>'+element.act+'</td>'+
//             '<td>'+element.prob+'</td>' +
//             '<td>add</td>'+
//             '</tr>');        
//         });

//     //    if(!initialized){
//         // $('#aoks').DataTable({
    
//         // });
//         // initialized = true;
//     //    }
            
      
        
//     });
// }
