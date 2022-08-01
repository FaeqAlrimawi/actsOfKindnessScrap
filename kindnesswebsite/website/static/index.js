
var global_row = -1;
var global_act = "";
// var initialized = false;


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
    // console.log("row: "+row +" act: " + act);
    
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
        
       
        let btn = $('#btn-'+row);
        message = data['message'];

        if(message == 'exists') {
            // console.log('act already exists in the database');
             btn.find('span').html('&#79;'); 
             btn.css("cursor", "default");
             btn.attr("onclick", "").unbind("click");
             btn.attr("title", "Already added");
             
        } else if (message == 'added'){
            btn.find('span').html('&#10004;'); 
            btn.css("cursor", "default");
            btn.attr("onclick", "").unbind("click");
            btn.attr("title", "Added successfully");

        } else if (message == 'error') {
        //    console.log('error adding the act');     
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
    // let spanValue = btnSpan.text();
    
     //if already added
    // if(spanValue === '&#10004;'){
        btnSpan.html('&plus;'); 
        btnRow.css("cursor", "pointer");
        btnRow.attr("onclick", "").unbind("click");
        btnRow.bind("click", function (){ add_AoK(row); });
        
    // } 
    fetch('/update-prob', {
        method: 'POST',
        body: JSON.stringify({aok: act}),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    }).then((response) => {
        return response.json();
   }).then((data) => {
        prob = data['prob'];
        // console.log("ooooo "+prob);
        var rounded = Math.round(prob * 100) / 100;
        $('#td-prob-'+row).html(rounded);
       
   });

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
