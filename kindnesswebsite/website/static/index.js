
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
        
        console.log(data);

        message = data['message'];

        if(message == 'exists') {
            console.log('act already exists in the database');
             $('#btn-'+row).find('span').html('&#10004;'); 
             $('#btn-'+row).css("cursor", "default");
             
        } else if (message == 'added'){
            //$('#btn-'+row).html("test"+result);
            $('#btn-'+row).find('span').html('&#10004;');
            //$('#btn-'+row).removeClass("btn btn-outline-dark").addClass("btn btn-success"); 
            $('#btn-'+row).css("cursor", "default");
            //  style= "cursor:pointer"
        } else if (message == 'error') {
           console.log('error adding the act');     
        }

        
        
    }

    ).catch(err => console.log(err));
}

function updateAoKText(row){

    var act = $('#txtarea-'+row).val();

    //alert(act);
    $('#td-'+row).html(act);
   
   $('#td-'+row).bind("click", function (){ update_AoK('+row+'); }); 

   global_act = act;
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
            
            '<button type="button"  class="btn btn-secondary" onClick="updateAoKText('+ row +')">Update</button>' +

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