document.addEventListener('DOMContentLoaded', function() {
    var dismissButtons = document.querySelectorAll('.close');
    dismissButtons.forEach(function(dismissButton) {
        dismissButton.addEventListener('click', function() {
            var alertElement = this.parentElement;
            alertElement.style.display = 'none';
        });
    });
});