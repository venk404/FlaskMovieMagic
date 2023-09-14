// script.js

function showDeleteConfirmation(event) {
    event.preventDefault();
    var confirmed = confirm("Are you sure you want to delete?");

    if (confirmed) {

        var id = event.target.getAttribute('href'); 
        event.target.href = id;
        window.location.href = id;
    } 
}
