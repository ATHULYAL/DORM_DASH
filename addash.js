document.addEventListener("DOMContentLoaded", function () {
    const noticeBoard = document.querySelector(".notice-board");
    
    // Sample notices stored in localStorage
    let notices = JSON.parse(localStorage.getItem("notices")) || [
        { title: "Last day of fee payment", message: "Make sure to clear all dues before the end of the month." },
        { title: "Farewell Party", message: "Join us to bid farewell to our seniors on January 30th." }
    ];
    
    function displayNotices() {
        // Remove existing notices before adding new ones
        const existingNotices = document.querySelectorAll(".notice");
        existingNotices.forEach(notice => notice.remove());
        
        notices.forEach((notice, index) => {
            const noticeDiv = document.createElement("div");
            noticeDiv.classList.add("notice");
            
            const title = document.createElement("p");
            title.innerHTML = `<strong>${notice.title}</strong>`;
            
            const message = document.createElement("p");
            message.textContent = notice.message;
            
            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.style.marginLeft = "10px";
            deleteBtn.style.cursor = "pointer";
            deleteBtn.style.background = "#d9534f";
            deleteBtn.style.color = "white";
            deleteBtn.style.border = "none";
            deleteBtn.style.padding = "5px 8px";
            deleteBtn.style.borderRadius = "4px";
            deleteBtn.style.fontSize = "1rem";
            
            deleteBtn.addEventListener("click", function () {
                notices.splice(index, 1);
                localStorage.setItem("notices", JSON.stringify(notices));
                displayNotices();
            });
            
            noticeDiv.appendChild(title);
            noticeDiv.appendChild(message);
            noticeDiv.appendChild(deleteBtn);
            
            noticeBoard.appendChild(noticeDiv);
        });
    }
    
    displayNotices();
    
    // Add new notice
    document.addEventListener("keydown", function (event) {
        if (event.key === "N" && event.ctrlKey) { // Press Ctrl + N to add a notice
            const title = prompt("Enter Notice Title:");
            const message = prompt("Enter Notice Message:");
            if (title && message) {
                notices.push({ title: title.trim(), message: message.trim() });
                localStorage.setItem("notices", JSON.stringify(notices));
                displayNotices();
            }
        }
    });
});

  
