let isEditing = false; // Variável para controlar o estado de edição

// Função para alternar o ícone e texto do botão
function toggleButton(button, isEditing) {
    if (isEditing) {
        button.querySelector('p').textContent = 'Salvar';
        button.querySelector('ion-icon').setAttribute('name', 'checkmark-outline');
    } else {
        button.querySelector('p').textContent = 'Editar';
        button.querySelector('ion-icon').setAttribute('name', 'pencil-outline');
    }
}

document.querySelectorAll('.btn-edit').forEach(button => {
    button.addEventListener('click', function () {
        const aniversarianteItem = button.closest('.aniversariante-item');
        const nameField = aniversarianteItem.querySelector('.namef');
        const dateField = aniversarianteItem.querySelector('#data-nascimento');

        if (!isEditing) {
            // Inicia a edição

            // Preenchendo o formulário de edição
            document.getElementById('nome_atual').value = nameField.textContent.trim();
            document.getElementById('edit_nome').value = nameField.textContent.trim();
            document.getElementById('edit_data_aniversario').value = dateField.textContent;

            // Exibe o formulário de edição
            document.getElementById('edit-form').style.display = 'block';

            // Mudar o texto do botão para "Salvar"
            toggleButton(this, true);

            // Atualizar o estado
            isEditing = true;
        } else {
            // Finaliza a edição (não faz nada aqui porque o formulário já está preenchido)

            // Mudar o texto do botão de volta para "Editar"
            toggleButton(this, false);

            // Atualizar o estado
            isEditing = false;
        }
    });
});
