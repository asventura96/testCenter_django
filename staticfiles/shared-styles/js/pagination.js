/* static/js/pagination.js */
document.addEventListener("DOMContentLoaded", function() {
    const recordsSelect = document.getElementById('records_per_page');
    if (recordsSelect) {
        recordsSelect.addEventListener('change', () => {
            document.querySelector('.pagination-form').submit();
        });
    }
});
