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

// Função para formatar o número de telefone enquanto o usuário digita
function formatarTelefone(input) {
    let valor = input.value.replace(/\D/g, ''); // Remove tudo que não é dígito
    if (valor.length > 10) {
        valor = valor.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
    } else if (valor.length > 5) {
        valor = valor.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
    } else if (valor.length > 2) {
        valor = valor.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        valor = valor.replace(/^(\d*)/, '($1');
    }
    input.value = valor;
}
