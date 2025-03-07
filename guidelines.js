document.getElementById("add-rule-btn").addEventListener("click", function () {
    let ruleName = prompt("Enter the name of the rule (e.g., Entry Timings):");
    if (!ruleName) return; 

    let ruleText = prompt("Enter the rule details:");
    if (!ruleText) return; 

    
    let newRule = document.createElement("li");
    newRule.innerHTML = `<strong>${ruleName}:</strong> ${ruleText} 
                         <button class="remove-btn">Remove</button>`;

    
    document.getElementById("rules-list").appendChild(newRule);

    
    newRule.querySelector(".remove-btn").addEventListener("click", function () {
        newRule.remove();
    });
});
