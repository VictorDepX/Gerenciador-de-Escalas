document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('toggleTheme');
    const htmlElement = document.documentElement;

    // Verifica se o tema preferido está salvo no localStorage
    if (localStorage.getItem('theme') === 'dark') {
        htmlElement.setAttribute('data-theme', 'dark');
    } else {
        htmlElement.setAttribute('data-theme', 'light');
    }

    // Adiciona um evento de clique no botão para alternar o tema
    toggleButton.addEventListener('click', function() {
        let currentTheme = htmlElement.getAttribute('data-theme');

        // Alterna entre os temas claro e escuro
        if (currentTheme === 'light') {
            htmlElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }
    });
});
