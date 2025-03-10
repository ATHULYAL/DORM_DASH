document.addEventListener("DOMContentLoaded", function () {
    const leaveForm = document.getElementById("leave-form");

    leaveForm.addEventListener("submit", function (event) {
        event.preventDefault(); 

       
        const hostelName = document.getElementById("hostel-name").value.trim();
        const studentName = document.getElementById("student-name").value.trim();
        const leaveStart = document.getElementById("leave-start").value;
        const leaveEnd = document.getElementById("leave-end").value;
        const purpose = document.getElementById("purpose").value.trim();
        const travelMode = document.getElementById("travel-mode").value;

        
        if (!hostelName || !studentName || !leaveStart || !leaveEnd || !purpose || !travelMode) {
            alert("Please fill in all fields before submitting.");
            return;
        }

        if (new Date(leaveStart) > new Date(leaveEnd)) {
            alert("Leave start date cannot be after the end date.");
            return;
        }

        
        const leaveRequest = {
            hostelName,
            studentName,
            leaveStart,
            leaveEnd,
            purpose,
            travelMode,
            submittedAt: new Date().toLocaleString()
        };

        
        let leaveRequests = JSON.parse(localStorage.getItem("leaveRequests")) || [];
        leaveRequests.push(leaveRequest);
        localStorage.setItem("leaveRequests", JSON.stringify(leaveRequests));

        
        alert(`Leave request for ${studentName} has been submitted successfully!`);

        
        leaveForm.reset();
    });
});
