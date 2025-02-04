document.addEventListener("DOMContentLoaded", function () {
    // Logout Functionality
    const logoutButton = document.querySelector('a[href="login.html"]');
    if (logoutButton) {
      logoutButton.addEventListener("click", function (event) {
        event.preventDefault();
        localStorage.removeItem("token"); // Clear stored token (if using authentication)
        alert("Logged out successfully!");
        window.location.href = "login.html"; // Redirect to login page
      });
    }
  
    // Highlight Active Sidebar Link
    const sidebarLinks = document.querySelectorAll(".sidebar a");
    sidebarLinks.forEach((link) => {
      if (link.href === window.location.href) {
        link.style.fontWeight = "bold";
        link.style.backgroundColor = "#3b5d6b";
      }
    });
  
    // Dynamic Notice Board (Simulated Data Fetch)
    const notices = [
      { title: "Hostel Maintenance", message: "Scheduled maintenance on Feb 10th." },
      { title: "Sports Meet", message: "Annual sports event on March 5th. Register now!" },
    ];
  
    const noticeBoard = document.querySelector(".notice-board");
    if (noticeBoard) {
      notices.forEach((notice) => {
        const noticeDiv = document.createElement("div");
        noticeDiv.classList.add("notice");
        noticeDiv.innerHTML = `<p><strong>${notice.title}</strong></p><p>${notice.message}</p>`;
        noticeBoard.appendChild(noticeDiv);
      });
    }
  });
  