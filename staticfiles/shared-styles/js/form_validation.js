// static/js/form_validation.js

document.addEventListener('DOMContentLoaded', function() {
    const nomeInput = document.getElementById('aluno-nome');

    nomeInput.addEventListener('input', function() {
        // Remove acentos e cedilha
        let nome = nomeInput.value;
        nome = nome.normalize("NFD").replace(/[\u0300-\u036f]/g, ""); // Remove acentos
        nome = nome.replace(/ç/g, 'c'); // Substitui cedilha por 'c'
        nome = nome.toUpperCase(); // Converte para maiúsculas

        nomeInput.value = nome; // Atualiza o valor do campo
    });
});
