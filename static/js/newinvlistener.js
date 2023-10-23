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
