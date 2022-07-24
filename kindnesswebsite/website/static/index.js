function delete_AoK(aokId){
    fetch('/delete-AoK', {
        method: 'POST',
        body: JSON.stringify({aokId: aokId})
    }).then((_res) => {
        window.location.href="/";
    });
}


$('#aok-form').click(function(event){
    // Prevent redirection with AJAX for contact form
    var form = $('#aok-form');
    var form_id = 'aok-form';
    var url = form.prop('action');
    var type = form.prop('method');
    var formData = getContactFormData(form_id);

    // submit form via AJAX
    send_form(form, form_id, url, type, modular_ajax, formData);
});

function getContactFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
//    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}