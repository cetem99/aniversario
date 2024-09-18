// Função para alternar a visibilidade da lista de aniversariantes
function toggleList() {
    var list = document.getElementById('aniversariantes-list');
    var btn = document.querySelector('.toggle-btn');

    if (list.classList.contains('hidden')) {
        list.classList.remove('hidden');
        btn.textContent = 'Esconder Aniversariantes';
    } else {
        list.classList.add('hidden');
        btn.textContent = 'Mostrar Aniversariantes';
    }
}
