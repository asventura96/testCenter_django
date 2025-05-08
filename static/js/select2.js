// static/js/select2.js
document.addEventListener("DOMContentLoaded", function() {
    if (typeof $.fn.select2 !== "undefined") {
        $('.select2').select2({
            placeholder: 'Selecione uma Opção',
            allowClear: true
        });
    } else {
        console.warn('Select2 não foi carregado corretamente.');
    }
});
