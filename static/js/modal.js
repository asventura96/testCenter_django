/* static/js/modal.js */
function openModal(modal) {
    modal.style.display = "block";
    requestAnimationFrame(() => modal.style.opacity = "1");
}

function closeModal(modal) {
    modal.style.opacity = "0";
    setTimeout(() => modal.style.display = "none", 300);
}

document.addEventListener("DOMContentLoaded", function() {
    $(document).on('click', '.btn-delete', function(event) {
        event.preventDefault();
        let itemPk = $(this).data('pk');
        let deleteUrl = '/delete/' + $(this).data('model') + '/' + itemPk + '/';
        $('.btn-confirm').data('pk', itemPk).data('url', deleteUrl);
        openModal(document.querySelector(".modal-delete"));
    });

    $(document).on('click', '.btn-confirm', function() {
        let deleteUrl = $(this).data('url');
        $.post(deleteUrl, { pk: $(this).data('pk'), csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() })
            .done(response => {
                showFeedback(response.success ? "Item excluído com sucesso." : "Erro ao excluir.", response.success);
                closeModal(document.querySelector(".modal-delete"));
            })
            .fail(() => showFeedback("Erro ao excluir.", false));
    });

    function showFeedback(message, isSuccess) {
        let modalFeedback = document.querySelector(".modal-feedback");
        modalFeedback.style.display = "block";
        modalFeedback.querySelector(".modal-feedback-message").textContent = message;
        setTimeout(() => closeModal(modalFeedback), 5000);
    }
});
