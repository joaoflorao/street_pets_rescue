function togglePasswordVisibility(togglePasswordId, passwordFieldId, toggleIconId) {
    const passwordField = document.getElementById(passwordFieldId);
    const toggleIcon = document.getElementById(toggleIconId);

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    }
}

function checkPasswordIsValid(){
    let password = document.getElementById('password');
    let confirm_password = document.getElementById('confirm_password');
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    password.setCustomValidity('');
    if (!passwordPattern.test(password.value)){
        password.setCustomValidity(
            "A senha deve conter no mínimo 8 caracteres, incluindo pelo menos uma letra maiúscula, "
            + "uma letra minúscula, um número e um símbolo especial."
        );
    }

    confirm_password.setCustomValidity('');
    if (confirm_password.value !== password.value){
        confirm_password.setCustomValidity('As senhas não coincidem!');
    }
}

function checkUserAge(){
    let elementBibirthDate = document.getElementById('birth_date');
    const birthDate = new Date(elementBibirthDate.value);
    const currentDate = new Date();

    let userAge = currentDate.getFullYear() - birthDate.getFullYear();
    const monthsDifference = currentDate.getMonth() - birthDate.getMonth();

    // Se o usuário ainda não fez aniversário no ano, é subtraído 1 da sua idade
    if (monthsDifference <= 0 && (currentDate.getDate() < birthDate.getDate())){
        userAge--;
    }
    elementBibirthDate.setCustomValidity('');
    if (userAge < 18){
        elementBibirthDate.setCustomValidity('Você deve ter no mínimo 18 anos.');
    }
}

function toggleStatusInput() {
    const actionType = document.getElementById("action_type").value;
    let statusSelectGroup = document.getElementById("status_select_group");
    let statusSelect = document.getElementById("status");

    statusSelectGroup.style.display = "none";
    if (actionType === "Alteração de status" || actionType === "Devolução de animal adotado") {
        statusSelect.required = true;
        statusSelectGroup.style.display = "block";
    }
}

function confirmSubmit(event, msgText) {
    event.preventDefault();

    Swal.fire({
        text: msgText,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Confirmar',
        cancelButtonText: 'Cancelar',
        buttonsStyling: true,
        reverseButtons: true,
        customClass: {
            confirmButton: 'btn btn-success',
            cancelButton: 'btn btn-danger'
        }
    }).then((result) => {
        if (result.isConfirmed) {
            event.target.submit();
        }
    });
}

function checkFileSize() {
    const fileInput = document.getElementById('animal_image');
    const file = fileInput.files[0];
    const maxSize = 25 * 1024 * 1024;

    if (file.size > maxSize) {
        alert('O arquivo deve ter no máximo 25 MB.');
        return false;
    }
    return true;
}
