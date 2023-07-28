const goToContactButton = document.querySelector('#goToContact');
const goToOptionsButton = document.querySelector('#goToOptions');
const contactPill = document.querySelector('#myTab button[data-bs-target="#pills-contact"]');
const optionsPill = document.querySelector('#myTab button[data-bs-target="#pills-options"]');
const submitButton = document.getElementById('submit-quote')

function showTab(tabElm){
    bootstrap.Tab.getOrCreateInstance(tabElm).show();
}

$(document).ready( async function() {
    goToContactButton.addEventListener('click', () => {
        showTab(contactPill);
    });
    goToOptionsButton.addEventListener('click', () => {
        showTab(optionsPill);
    });
});

function updateElementIndex(el, prefix, ndx) {
    let id_regex = new RegExp('(' + prefix + '-\\d+)');
    let replacement = prefix + '-' + ndx;
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function copy_form_content(from_form_no, to_form_no) {
    let forms = $('.quote-item-row');
    let from_form = $(forms[from_form_no])
    let to_form = $(forms[to_form_no])
    let from_inputs = from_form.find(':input')
    let to_inputs = to_form.find(':input')
    for (let i=0, input_count=from_inputs.length; i<input_count; i++) {
        if (from_inputs[i].type === "checkbox") {
            to_inputs[i].checked = from_inputs[i].checked
        } else {
            to_inputs[i].value = from_inputs[i].value
        }
        to_inputs[i].dispatchEvent(new Event('change'));
    }
}

function deleteForm(prefix, btn) {
    let total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    if (total > 1){
        btn.closest('.quote-item-row').remove();
        let forms = $('.quote-item-row');
        let total_forms = forms.length - 1;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total_forms);
        for (let i=0, formCount=total_forms; i<formCount; i++) {
            let form = $(forms[i]);
            form.find(':input').each(function() {
                updateElementIndex(this, prefix, i);
            });
            form.find("h4")[0].innerHTML = `Asset ${i+1}`;
        }
    }
    return false;
}

function add_form() {
    let form_idx = parseInt($('#id_form-TOTAL_FORMS').val());
    $('#form-set').append($('#empty-form').html().replace(/__prefix__/g, form_idx));
    $('#id_form-TOTAL_FORMS').val(form_idx + 1);

    let forms = $('.quote-item-row');
    let total_forms = forms.length;
    $('#id_' + form_idx + '-TOTAL_FORMS').val(total_forms);
    for (let i = 0, formCount = total_forms; i < formCount - 1; i++) {
        let form = $(forms[i]);
        form.find("h4")[0].innerHTML = `Asset ${i+1}`;
    }
}

$(document).on('click', '.clone-w', function(){
    add_form();
    let copy_idx = $('#id_form-TOTAL_FORMS').val() - 2;
    copy_form_content(copy_idx, copy_idx + 1);
})

$(document).on('click', '.add-w', function(e){
    add_form();
});

$(document).on('click', '.remove-form-row', function(e){
    deleteForm('form', $(this));
    return false;
});



