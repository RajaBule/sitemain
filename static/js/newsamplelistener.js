document.addEventListener('DOMContentLoaded', function () {
    console.log("JavaScript code executing");
    //submit button
    const submitButton = document.getElementById('submit-button');
    const form = document.getElementById('newsample');

    submitButton.addEventListener('submit', function(event) {
        //event.preventDefault();  // Prevent the default link behavior
        form.submit();  // Submit the form programmatically
        console.log("submiting...");
    });
    // Dropdown 1
    const customDropdownButtons = document.querySelectorAll('[data-toggle="sampledropdown"]');
    const dropdownButton1 = document.getElementById('sampledrop'); //<!-- btn id -->
    const selectedOptionInput1 = document.getElementById('stype'); //<!-- input id-->
    
    dropdownButton1.addEventListener('click', function () {
        const dropdown = document.querySelector(`[data-dropdown="${this.getAttribute('data-toggle')}"]`);
        dropdown.classList.toggle('show');
    });

    const dropdownItems1 = document.querySelectorAll('[data-dropdown="datadropsample"] a');
    dropdownItems1.forEach(function (item) {
        item.addEventListener('click', function () {
            const selectedText = item.textContent.trim();
            dropdownButton1.textContent = selectedText;
            selectedOptionInput1.value = selectedText;
        });
    });

    // Dropdown 2
    const customDropdownButtons2 = document.querySelectorAll('[data-toggle="weightdatadrop"]');
    const dropdownButton2 = document.getElementById('weightdrop');
    const selectedOptionInput2 = document.getElementById('sampleweightunit');
    
    dropdownButton2.addEventListener('click', function () {
        const dropdown = document.querySelector(`[data-dropdown="${this.getAttribute('data-toggle')}"]`);
        dropdown.classList.toggle('show');
    });

    const dropdownItems2 = document.querySelectorAll('[data-dropdown="weightdatadrop"] a');
    dropdownItems2.forEach(function (item) {
        item.addEventListener('click', function () {
            const selectedText = item.textContent.trim();
            dropdownButton2.textContent = "Sample Weight" + ' (' + selectedText + ')';
            selectedOptionInput2.value = selectedText;
        });
    });

    // Dropdown 3
    const customDropdownButtons3 = document.querySelectorAll('[data-toggle="weightdatadrop2"]');
    const dropdownButton3 = document.getElementById('weightdrop2');
    const selectedOptionInput3 = document.getElementById('expweightunit');
    
    dropdownButton3.addEventListener('click', function () {
        const dropdown = document.querySelector(`[data-dropdown="${this.getAttribute('data-toggle')}"]`);
        dropdown.classList.toggle('show');
    });

    const dropdownItems3 = document.querySelectorAll('[data-dropdown="weightdatadrop2"] a');
    dropdownItems3.forEach(function (item) {
        item.addEventListener('click', function () {
            const selectedText = item.textContent.trim();
            dropdownButton3.textContent = "Availability" + ' (' + selectedText + ')';
            selectedOptionInput3.value = selectedText;
        });
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
