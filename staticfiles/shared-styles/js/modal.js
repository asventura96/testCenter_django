// static/js/modal.js

$(document).ready(function() {
    var modalDelete = $('.modal-delete');
    var modalFeedback = $('.modal-feedback');
    var feedbackMessage = $('.modal-feedback-message');
    var countdownMessage = $('.countdown-message');

    // Função para fechar modais
    function closeModals() {
        modalDelete.hide();
        modalFeedback.hide();
        feedbackMessage.text('');
        countdownMessage.text('');
    }

    // Captura clique no botão de excluir
    $('.btn-delete').on('click', function(event) {
        event.preventDefault();  // Impede o redirecionamento direto

        var url = $(this).attr('href') || $(this).data('url');
        var redirectUrl = $(this).data('redirect-url');
        if (!url) {
            alert('URL de exclusão não encontrada.');
            return;
        }

        modalDelete.show();

        // Armazena a URL para usar na confirmação
        modalDelete.data('url', url);
        modalDelete.data('redirect-url', redirectUrl);
    });

    // Fechar modal ao clicar no botão fechar ou cancelar
    $('.btn-close-modal, .btn-cancel').on('click', function() {
        closeModals();
    });

    // Confirmar exclusão via AJAX
    $('.btn-confirm').on('click', function() {
        var url = modalDelete.data('url');
        var redirectUrl = modalDelete.data('redirect-url');
        if (!url) return;

        // Obtém o token CSRF do cookie ou meta tag
        var csrftoken = getCookie('csrftoken');

        $.ajax({
            url: url,
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': csrftoken
            },
            success: function(response) {
                modalDelete.hide();

                if (response.success) {
                    feedbackMessage.html(response.message);
                    countdownMessage.html('Você será redirecionado para a lista em <strong>3</strong> segundos...');
                    modalFeedback.show();

                    var countdown = 3;
                    var interval = setInterval(function() {
                        countdown--;
                        countdownMessage.html('Você será redirecionado para a lista em <strong>' + countdown + '</strong> segundos...');
                        if (countdown <= 0) {
                            clearInterval(interval);
                            window.location.href = redirectUrl;
                        }
                    }, 1000);
                } else {
                    feedbackMessage.html(response.message);
                    countdownMessage.html('');
                    modalFeedback.show();
                }
            },
            error: function() {
                modalDelete.hide();
                feedbackMessage.html('Erro inesperado ao tentar excluir o cliente.');
                countdownMessage.html('');
                modalFeedback.show();
            }
        });
    });

    // Função para obter o cookie CSRF (padrão Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i=0; i<cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Verifica se o cookie começa com o nome procurado
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
