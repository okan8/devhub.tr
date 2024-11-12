function checkPasswordStrength() {
    const password = document.getElementById("registerPassword").value;
    const minLength = document.getElementById("minLength");
    const uppercase = document.getElementById("uppercase");
    const lowercase = document.getElementById("lowercase");
    const number = document.getElementById("number");
    const specialChar = document.getElementById("specialChar");

    const uppercaseRegEx = /[A-Z]/;
    const lowercaseRegEx = /[a-z]/;
    const numberRegEx = /[0-9]/;
    const specialCharRegEx = /[!@#$%^&*(),.?":{}|<>]/;

    // Kontrolleri gerçekleştir
    minLength.classList.toggle("text-green-500", password.length >= 8);
    uppercase.classList.toggle("text-green-500", uppercaseRegEx.test(password));
    lowercase.classList.toggle("text-green-500", lowercaseRegEx.test(password));
    number.classList.toggle("text-green-500", numberRegEx.test(password));
    specialChar.classList.toggle("text-green-500", specialCharRegEx.test(password));

    // Şartları kontrol et
    const allConditionsMet =
        password.length >= 8 &&
        uppercaseRegEx.test(password) &&
        lowercaseRegEx.test(password) &&
        numberRegEx.test(password) &&
        specialCharRegEx.test(password);

    document.getElementById("registerButton").disabled = !allConditionsMet;
}

// Kayıt işlemi
document.getElementById('registerButton').addEventListener('click', async function () {
    const email = document.getElementById('registerEmail').value;
    const password = document.getElementById('registerPassword').value;
    const messageDiv = document.getElementById('registerMessage');

    const response = await fetch('register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    // Check response status and display appropriate messages
    if (response.status === 200) {
        messageDiv.classList.add('text-green-500');
        messageDiv.textContent = "Kayıt başarılı! Giriş yapabilirsiniz.";
    } else {
        messageDiv.classList.add('text-red-500');
        messageDiv.textContent = data.message || "Kayıt sırasında hata oluştu. Lütfen tekrar deneyin.";
    }
});

// Giriş işlemi
document.getElementById('loginButton').addEventListener('click', async function () {
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const messageDiv = document.getElementById('loginMessage');

    const response = await fetch('login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email:email, password:password })
    });

    const data = await response.json();
    
    // Check response status and display appropriate messages
    if (response.status === 200) {
        messageDiv.classList.add('text-green-500');
        window.location.href="/dashboard"
    } else {
        messageDiv.classList.add('text-red-500');
    }
    messageDiv.textContent = data["message"]

});

// Kayıt ve giriş sekmeleri
document.getElementById('showRegister').addEventListener('click', function () {
    document.getElementById('registerSection').classList.remove('hidden');
    document.getElementById('loginSection').classList.add('hidden');
});

document.getElementById('showLogin').addEventListener('click', function () {
    document.getElementById('loginSection').classList.remove('hidden');
    document.getElementById('registerSection').classList.add('hidden');
});