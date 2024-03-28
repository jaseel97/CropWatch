// script.js

function showLoginForm() {
    document.getElementById("login-form").classList.add("active");
    document.getElementById("register-form").classList.remove("active");
}

function showRegisterForm() {
    document.getElementById("login-form").classList.remove("active");
    document.getElementById("register-form").classList.add("active");
}

function login() {
    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;

    const storedUsername = localStorage.getItem("username");
    const storedPassword = localStorage.getItem("password");

    if (username === storedUsername && password === storedPassword) {
        // Redirect to the menu page
        window.location.href = "menu.html";
    } else {
        alert("Invalid username or password.");
    }
}

function register() {
    const username = document.getElementById("register-username").value;
    const password = document.getElementById("register-password").value;

    localStorage.setItem("username", username);
    localStorage.setItem("password", password);

    alert("Registration successful!");
    showLoginForm(); // Switch back to login form after registration
}

// Display the login form by default
showLoginForm();
