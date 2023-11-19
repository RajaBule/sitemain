document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript code executing");
    //submit button
    const submitButton = document.getElementById('submit-button');
    const form = document.getElementById('newinventory');

    submitButton.addEventListener('submit', function(event) {
        //event.preventDefault();  // Prevent the default link behavior
        form.submit();  // Submit the form programmatically
        console.log("submiting...");
    });

    // Dropdown 4
    const customDropdownButtons4 = document.querySelectorAll('[data-toggle="weightdatadrop3"]');
    const dropdownButton4 = document.getElementById('weightdrop3');
    const selectedOptionInput4 = document.getElementById('proccessing');
    
    dropdownButton4.addEventListener('click', function () {
        const dropdown = document.querySelector(`[data-dropdown="${this.getAttribute('data-toggle')}"]`);
        dropdown.classList.toggle('show');
    });

    const dropdownItems4 = document.querySelectorAll('[data-dropdown="weightdatadrop3"] a');
    dropdownItems4.forEach(function (item) {
        item.addEventListener('click', function () {
            const selectedText = item.textContent.trim();
            dropdownButton4.textContent = selectedText;
            selectedOptionInput4.value = selectedText;
        });
    });
});


    // Function to calculate and update the Total Inventory
function updateTotal() {
        // Get all the grade input elements and the "unsortedq" and "defectq" inputs
    var gradeInputs = document.querySelectorAll('[name^="g"]');
    var unsortedInput = document.querySelector('[name="unsortedq"]');
    var defectInput = document.querySelector('[name="defectq"]');
        
    var total = 0;

        // Iterate through all grade inputs, "unsortedq," and "defectq" inputs and calculate the sum
    gradeInputs.forEach(function(gradeInput) {
        var value = parseFloat(gradeInput.value) || 0;
        total += value;
    });

        // Add the values of "unsortedq" and "defectq" to the total
    total += (parseFloat(unsortedInput.value) || 0);
    total += (parseFloat(defectInput.value) || 0);

        // Update the Total Inventory input with the calculated sum
    var totalInput = document.querySelector('[name="totalq"]');
    totalInput.value = total;
    }

    // Attach an event listener to each grade input, "unsortedq," and "defectq" to update the Total Inventory when any of them change
    var gradeInputs = document.querySelectorAll('[name^="g"]');
    var unsortedInput = document.querySelector('[name="unsortedq"]');
    var defectInput = document.querySelector('[name="defectq"]');
    
    gradeInputs.forEach(function(gradeInput) {
        gradeInput.addEventListener('input', updateTotal);
    });
    
    unsortedInput.addEventListener('input', updateTotal);
    defectInput.addEventListener('input', updateTotal);
