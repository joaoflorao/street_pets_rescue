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
    const password = document.getElementById('password');
    const confirm_password = document.getElementById('confirm_password');
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!passwordPattern.test(password.value)){
        password.setCustomValidity(
            "A senha deve conter no mínimo 8 caracteres, incluindo pelo menos uma letra maiúscula, "
            + "uma letra minúscula, um número e um símbolo especial."
        );
    }
    else{
        password.setCustomValidity('');
    }

    if (confirm_password.value !== password.value){
        confirm_password.setCustomValidity('As senhas não coincidem!');
    }
    else{
        confirm_password.setCustomValidity('');
    }
}

function checkUserAge(){
    const elementBibirthDate = document.getElementById('birth_date');
    const birthDate = new Date(elementBibirthDate.value);
    const currentDate = new Date();

    let userAge = currentDate.getFullYear() - birthDate.getFullYear();
    const monthsDifference = currentDate.getMonth() - birthDate.getMonth();

    // Se o usuário ainda não fez aniversário no ano, é subtraído 1 da sua idade
    if (monthsDifference <= 0 && (currentDate.getDate() < birthDate.getDate())){
        userAge--;
    }
    if (userAge < 18){
        elementBibirthDate.setCustomValidity('Você deve ter no mínimo 18 anos.');
    }
}