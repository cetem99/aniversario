let isEditing = false; // Variável para controlar o estado de edição

document.querySelector('.btn-edit').addEventListener('click', function() {
    const nameField = document.querySelector('.namef');
    const dateField = document.getElementById('data-nascimento');

    if (!isEditing) {
        // Inicia a edição (transforma os <h2> em <input>)

        // Transformar o nome (h2) em input
        const inputName = document.createElement('input');
        inputName.type = 'text';
        inputName.value = nameField.textContent;
        inputName.classList.add('namef-input');
        inputName.setAttribute('id', 'input-name');

        // Transformar a data de nascimento (h2) em input
        const inputDate = document.createElement('input');
        inputDate.type = 'text';  // Pode alterar para 'date' se preferir
        inputDate.value = dateField.textContent;
        inputDate.classList.add('data-nascimento-input');
        inputDate.setAttribute('id', 'input-date');

        // Substituir os <h2> pelos <input>
        nameField.replaceWith(inputName);
        dateField.replaceWith(inputDate);

        // Mudar o texto do botão para "Salvar"
        this.querySelector('p').textContent = 'Salvar';
        this.querySelector('ion-icon').setAttribute('name', 'checkmark-outline');

        // Atualizar o estado
        isEditing = true;
    } else {
        // Finaliza a edição (transforma os <input> de volta em <h2>)

        const inputName = document.getElementById('input-name');
        const inputDate = document.getElementById('input-date');

        // Criar novos <h2> com os valores dos inputs
        const newName = document.createElement('h2');
        newName.classList.add('namef');
        newName.textContent = inputName.value;

        const newDate = document.createElement('h2');
        newDate.id = 'data-nascimento';
        newDate.textContent = inputDate.value;

        // Substituir os <input> pelos novos <h2>
        inputName.replaceWith(newName);
        inputDate.replaceWith(newDate);

        // Mudar o texto do botão de volta para "Editar"
        this.querySelector('p').textContent = 'Editar';
        this.querySelector('ion-icon').setAttribute('name', 'pencil-outline');

        // Atualizar o estado
        isEditing = false;
    }
});