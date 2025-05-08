/* static/js/checkbox-toggle.js */
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('input[type="checkbox"][data-target]').forEach(checkbox => {
        const targetField = document.getElementById(checkbox.dataset.target);
        if (targetField) {
            targetField.disabled = !checkbox.checked;
            checkbox.addEventListener('change', () => {
                targetField.disabled = !checkbox.checked;
                if (!checkbox.checked) targetField.value = '';
            });
        }
    });
});
