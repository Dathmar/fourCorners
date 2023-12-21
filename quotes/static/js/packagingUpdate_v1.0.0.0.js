const submitButtons = document.getElementsByClassName("submit-package")

document.addEventListener("DOMContentLoaded", (event) => {
    for (let i = 0; i < submitButtons.length; i++) {
        submitButtons[i].addEventListener("click", function() {
            move_quote_to_packaged(this);
        });
    }

});

async function move_quote_to_packaged(btn) {
    let quote_id = btn.value;
    btn.disabled = true;
    let col = btn.parentElement;
    const response = await fetch(`/api/v1/move-quote-to-packaged/${quote_id}/`, {
        method: 'POST',
        headers: {"X-Requested-With": "XMLHttpRequest", "X-CSRFToken": getCookie("csrftoken")},
    });
    if (response.status === 200) {

        col.innerHTML = '<p>Packaging Complete</p>'
    } else {
        col.innerHTML = `<p>Error moving package to complete.  Reload the page and try again</p><p>Error id ${response.status}</p>`
    }
    return;
}