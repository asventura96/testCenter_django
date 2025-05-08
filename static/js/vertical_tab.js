/* static/js/vertical_tab.js */
document.addEventListener('DOMContentLoaded', () => {
    const tabs = document.querySelectorAll('.verticalTab');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const contentId = tab.getAttribute('data-content');
            showContent(contentId);
        });
    });
});

function showContent(contentId) {
    // Esconde todos os itens de conteúdo
    const contentItems = document.querySelectorAll('.verticalTab-content-item');
    contentItems.forEach(item => {
        item.classList.remove('active');
    });

    // Mostra o conteúdo correspondente à aba clicada
    const activeContent = document.getElementById(contentId);
    activeContent.classList.add('active');
}
