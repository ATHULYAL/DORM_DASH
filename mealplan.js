document.addEventListener("DOMContentLoaded", function () {
    const mealPlanForm = document.querySelector("form");

    mealPlanForm.addEventListener("submit", function (event) {
        event.preventDefault(); 

       
        const date = document.getElementById("date").value;
        const fileInput = document.getElementById("file");

        
        if (!date || !fileInput.files.length) {
            alert("Please select a date and upload a file before submitting.");
            return;
        }

       
        const file = fileInput.files[0];

        
        const reader = new FileReader();
        reader.onload = function (e) {
            const mealPlanData = {
                date,
                fileName: file.name,
                fileData: e.target.result, 
                submittedAt: new Date().toLocaleString()
            };

            
            let mealPlans = JSON.parse(localStorage.getItem("mealPlans")) || [];
            mealPlans.push(mealPlanData);
            localStorage.setItem("mealPlans", JSON.stringify(mealPlans));

           
            alert(`Meal Plan for ${date} has been uploaded successfully!`);

           
            mealPlanForm.reset();
        };

        reader.readAsDataURL(file); 
    });
});
