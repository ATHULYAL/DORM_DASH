document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.querySelector("form");
  
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault();
  
      const username = document.getElementById("username").value.trim();
      const password = document.getElementById("password").value.trim();
  
      if (username === "" || password === "") {
        alert("Please fill in both fields.");
        return;
      }
  
      // Simulated login validation
      if (username === "admin" && password === "password123") {
        alert("Login successful!");
        window.location.href = "addash.html"; // Redirect to dashboard
      } else {
        alert("Invalid username or password.");
      }
    });
  });
  