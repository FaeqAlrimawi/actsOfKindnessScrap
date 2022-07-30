
var global_row = -1;
var global_act = "";


function delete_AoK(aokId){
    fetch('/delete-AoK', {
        method: 'POST',
        body: JSON.stringify({aokId: aokId})
    }).then((_res) => {
        window.location.href="/edit";
    });
}


function add_AoK(row){

    var act = $('#td-'+row).text();
    
    fetch('/add-AoK', {
        method: 'POST',
        body: JSON.stringify({aok: act, row:row}),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => {

        return response.json();        
    }).then((data) => {
        
        // console.log(data);
        let btn = $('#btn-'+row);
        message = data['message'];

        if(message == 'exists') {
            console.log('act already exists in the database');
             btn.find('span').html('&#10004;'); 
             btn.css("cursor", "default");
             btn.attr("onclick", "").unbind("click");
             
        } else if (message == 'added'){
            btn.find('span').html('&#10004;'); 
            btn.css("cursor", "default");
            btn.attr("onclick", "").unbind("click");
        } else if (message == 'error') {
           console.log('error adding the act');     
        }

        
        
    }

    ).catch(err => console.log(err));
}

function updateAoKText(row, old_act){

    var act = $('#txtarea-'+row).val();

    //alert(act);
    $('#td-'+row).html(act);
   
   $('#td-'+row).bind("click", function (){ update_AoK('+row+'); }); 

   global_act = act;

   //update add button if needed
   btnRow = $('#btn-'+row);

   if(act !== old_act) {
    let btnSpan = btnRow.find('span');
    let spanValue = btnSpan.text();
    console.log("checking if need to update button, span: " + spanValue);
     //if already added
    // if(spanValue === '&#10004;'){
        btnSpan.html('&plus;'); 
        btnRow.css("cursor", "pointer");
        btnRow.bind("click", function (){ add_AoK('+row+'); });
        console.log("changing the add button to ADD");
    // } 
   }

   
}


function cancelAoKUpdate(act, row){

   
    $('#td-'+row).html(act);

    
    $('#td-'+row).bind("click", function (){ update_AoK('+row+'); });

    
}

function cancelAoKUpdateESC(e, act, row){

    e = e || window.event;
    var code = e.keyCode;

    if(code == 27) {
        cancelAoKUpdate(act, row);
    }

 

}

function update_AoK(row){

    var act = $('#td-'+row).text().trim();

    if(global_row != -1) {
        $('#td-'+global_row).html(global_act);
        
        $('#td-'+global_row).attr("onclick", 'update_AoK('+global_row+')').bind("click");
        
    }


        $('#td-'+row).html('<div align="left" style="width:100%;"> ' +
            '<textarea  name="act"  id="txtarea-'+row+ '" onKeyDown="cancelAoKUpdateESC(event, \''+act+'\',' + row +')" style="width:100%">'+act+'</textarea>' +
            
            '<button type="button"  class="btn btn-secondary" onClick="updateAoKText('+ row + ',\''+act+'\'' + ')">Update</button>' +

            '&nbsp;&nbsp;' +
            
            '<button type="button"  class="btn btn-secondary" onClick="cancelAoKUpdate(\''+act+'\',' + row +')">Cancel</button>' +
            
            '</div>');
        
        $('#td-'+row).attr("onclick", "").unbind("click");

        $('#txtarea-'+row).focus();
        
        global_row = row;
        global_act = act;
   
}


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