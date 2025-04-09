document.addEventListener("DOMContentLoaded", function () {
    console.log("Student Fee Page Loaded");

    const gridItems = document.querySelectorAll(".grid-item");

    gridItems.forEach((item) => {
        item.addEventListener("click", function () {
            const action = this.textContent.trim().toLowerCase().replace(" ", "_");
            handleFeeAction(action);
        });
    });

    function handleFeeAction(action) {
        switch (action) {
            case "view_fees":
                alert("Viewing Fees...");
                break;
            case "payment":
                alert("Proceeding to Payment...");
                break;
            case "payment_history":
                alert("Fetching Payment History...");
                break;
            case "pending_fees":
                alert("Checking Pending Fees...");
                break;
            case "overdue_fees":
                alert("Fetching Overdue Fees...");
                break;
            case "download_receipt":
                alert("Downloading Receipt...");
                break;
            default:
                console.error("Unknown action: " + action);
        }
    }
});
