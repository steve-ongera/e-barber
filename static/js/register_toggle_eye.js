// Toggle Password Visibility for Password1
const passwordInput1 = document.getElementById('password1');
const eyeIcon1 = document.getElementById('eyeIcon1');

eyeIcon1.addEventListener('click', () => {
    const type = passwordInput1.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput1.setAttribute('type', type);
    eyeIcon1.classList.toggle('bi-eye');
    eyeIcon1.classList.toggle('bi-eye-slash');
});

// Toggle Password Visibility for Password2
const passwordInput2 = document.getElementById('password2');
const eyeIcon2 = document.getElementById('eyeIcon2');

eyeIcon2.addEventListener('click', () => {
    const type = passwordInput2.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordInput2.setAttribute('type', type);
    eyeIcon2.classList.toggle('bi-eye');
    eyeIcon2.classList.toggle('bi-eye-slash');
});
