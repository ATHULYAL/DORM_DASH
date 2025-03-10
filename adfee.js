document.addEventListener("DOMContentLoaded", function () {
    const gridItems = document.querySelectorAll(".grid-item");
    
    gridItems.forEach(item => {
        item.addEventListener("click", function () {
            const action = this.textContent.toLowerCase();
            handleFeeAction(action);
        });
    });

    function handleFeeAction(action) {
        switch (action) {
            case "view":
                window.location.href = "view_fees.html";
                break;
            case "add":
                window.location.href = "add_fees.html";
                break;
            case "approval":
                window.location.href = "approval_fees.html";
                break;
            case "pending":
                alert("Displaying pending fees (Feature to be implemented)");
                break;
            case "overdues":
                alert("Showing overdue fees (Feature to be implemented)");
                break;
            case "report":
                alert("Generating fee report (Feature to be implemented)");
                break;
            default:
                console.log("Unknown action: " + action);
        }
    }
});
