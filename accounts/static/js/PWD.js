document.addEventListener("DOMContentLoaded", function () {

    const toggle = document.querySelector("#togglePassword");
    const password = document.querySelector("#password");

    if (toggle && password) {
        toggle.addEventListener("click", function () {

            const type = password.getAttribute("type") === "password" ? "text" : "password";
            password.setAttribute("type", type);

            // toggle icon
            this.classList.toggle("fa-eye-slash");
            this.classList.toggle("fa-eye");
        });
    }

});

