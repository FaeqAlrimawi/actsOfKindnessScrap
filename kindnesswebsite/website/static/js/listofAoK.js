var gridOptions = null;


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
  
  

function fillActsGrid() {


    if(gridOptions == null) {
        createAoKsGrid();
    }

    fetch("/api/aokdata", { 
    method: 'POST',
    body: JSON.stringify({operation:'fetch-all'}),
    cache: "no-cache",
    headers: new Headers({
        "content-type": "application/json"
    })
    })
  .then(response => response.json())
  .then(data => {
    // load fetched data into grid
    // console.log(data[0]);
    gridOptions.api.setRowData(data);
  });

}


function createAoKsGrid() {
    // console.log("create grid");
  // Grid Options are properties passed to the grid
   gridOptions = {

    // each entry here represents one column
    columnDefs: [
      { field: "id", hide:true }, 
     
      { field: "act",  headerName:"AoK", editable: false, minWidth:700},
      { field: "source",  headerName:"Source", editable: false, cellRenderer:function(params) {

        let source = params.data.source;

        if(source != null) {
            return `<a href="${source}" target=_blank">${source}</a>`;
        }

        return;
        
    }
},
      { field: "date",  headerName:"Date Added", editable: false}    
    ],

    
    onFirstDataRendered: headerHeightSetter,
    onColumnResized: headerHeightSetter,

    onGridSizeChanged: () => {
      gridOptions.api.sizeColumnsToFit();
  } ,    

    // default col def properties get applied to all columns
    defaultColDef: {sortable: true, filter: true,  wrapText: true,  
    autoHeight: true, resizable: true, cellClass: 'locked-col',  lockPosition: 'left'},
    
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

  // gridOptions.api.hideOverlay();
  // Fetch data from server
  // fetch("/api/actdata")
  // .then(response => response.json())
  // .then(data => {
  //   // load fetched data into grid
  //   // console.log(data[0]);
  //   gridOptions.api.setRowData(data);
  // });
}

function hrefSource(params) {

    return "<a href=\""+params.source+"\" target=_blank">+params.source+"</a>";
}