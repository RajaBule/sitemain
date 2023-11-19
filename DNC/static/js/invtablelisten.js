document.addEventListener('DOMContentLoaded', function() {
    const selectElement = document.getElementById('maxrange');
    const searchInput = document.querySelector('input[id="tablesearch"]');
    const dataTableBody = document.querySelector('#dataTable tbody');
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    const currentUrl = window.location.href;

    // Get the selected value from the URL's query parameters
    const urlSearchParams = new URLSearchParams(window.location.search);
    const selectedValueFromURL = urlSearchParams.get('selected');
    if (selectedValueFromURL) {
        selectElement.value = selectedValueFromURL;
    }

    // Attach event listener to checkboxes
    function attachCheckboxEventListeners() {
        $('#dataTable input[type="checkbox"]').on('change', function() {
            const selectedRowID = $(this).val();
            if ($(this).is(':checked')) {
                selectedRowIDs.push(selectedRowID);
            } else {
                const index = selectedRowIDs.indexOf(selectedRowID);
                if (index !== -1) {
                    selectedRowIDs.splice(index, 1);
                }
            }
            console.log('Selected row IDs:', selectedRowIDs);
        });
    }

    attachCheckboxEventListeners();

    function updateTableContent(data) {
        const dataTableBody = document.querySelector('#dataTable tbody');
        dataTableBody.innerHTML = ''; // Clear existing table rows

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="width: 85px;max-width: 100px;"><input class="form-check-input custom-control-input" type="checkbox" value=${item.id}></td>
                <td>${item.id}</td>
                <td><a href="${item.ref}">${item.name}</a></td>
                <td>${item.location}</td>
                <td>${item.sensorial}</td>
                <td>${item.sensorialdescriptors}</td>
                <td>${item.regdate}</td>
            `;
            dataTableBody.appendChild(row);
        });

        attachCheckboxEventListeners();
    }

    selectElement.addEventListener('change', function() {
        const selectedValue = selectElement.value;
        const urlWithSelectedValue = updateQueryStringParameter(currentUrl, 'selected', selectedValue);
        console.log('select value:', urlWithSelectedValue);
        window.location.href = urlWithSelectedValue;
    });

    updatePaginationLinks(selectElement.value);
    searchInput.addEventListener('input', function() {
        const searchQuery = searchInput.value;
        const selectedValue = selectElement.value;
        // Make an AJAX request to the Django view
        $.ajax({
            url: `/searchinv/?q=${searchQuery}&selected=${selectedValue}`, // Modify the URL as needed
            dataType: 'json',
            success: function(data) {
                // Update the table content with the search results
                updateTableContent(data);
            }
        });
    });

    selectAllCheckbox.addEventListener('change', function() {
        const checkboxes = dataTableBody.querySelectorAll('input[type="checkbox"]');
        checkboxes.forEach(checkbox => {
            checkbox.checked = selectAllCheckbox.checked;
        });
    });

    const selectedRowIDs = [];

    $('#edit-selected').on('click', function() {
        const selectedRowIDsString = selectedRowIDs.join(',');
        const editSelectedURL = 'edit_selected/';
        console.log('url:', editSelectedURL);
        window.location.href = `${editSelectedURL}?ids=${selectedRowIDsString}`;
    });

    // Handle "Start Cupping Selected" option
    $('#start-cupping-selected').on('click', function() {
        if (selectedRowIDs.length > 0) {
            const selectedRowIDsString = selectedRowIDs.join(',');
            const cuppingSciURL = 'cupping_sci/';
            // Append the selected sample IDs as a query parameter
            const urlWithSelectedIDs = `${cuppingSciURL}?selected_ids=${selectedRowIDsString}`;
            // Redirect to the "cupping_sci" page with the selected IDs
            window.location.href = urlWithSelectedIDs;
        } else {
            // Handle the case where no samples are selected
            alert('No samples are selected for cupping.');
        }
    });

    function updatePaginationLinks(selectedValue) {
        const paginationLinks = document.querySelectorAll('.page-link');
        paginationLinks.forEach(link => {
            const pageUrl = updateQueryStringParameter(link.getAttribute('href'), 'selected', selectedValue);
            link.setAttribute('href', pageUrl);
        });
    }

    function updateQueryStringParameter(uri, key, value) {
        const re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
        const separator = uri.indexOf('?') !== -1 ? "&" : "?";
        if (uri.match(re)) {
            return uri.replace(re, '$1' + key + "=" + value + '$2');
        }
        return uri + separator + key + "=" + value;
    }

    $(document).ready(function () {
        const searchInput = $('input[name="sharesearch"]');
        const tableBody = $('#username_search tbody'); // Select the table element
        const tablediv = $('#table_div');

        searchInput.on('input', function () {
            const searchQuery = searchInput.val();
            console.log('Searching');
            $.ajax({
                url: 'search_users/',
                data: { 'search_query': searchQuery },
                dataType: 'json',
                success: function (data) {
                    const users = data.users;
                    tableBody.empty(); // Clear existing table rows

                    if (users.length > 0) {
                        $.each(users, function (index, user) {
                            const row = $('<tr data-username-id="' + user.id + '"><td>' + user.username + '</td></tr>');
                            tableBody.append(row);
                        });
                    } else {
                        // Handle case when no users are found
                        const row = $('<tr><td>No users found.</td></tr>');
                        tableBody.append(row);
                    }

                    // Update the class attribute based on search results
                    if (searchQuery.length > 0) {
                        tablediv.removeClass('d-none');
                    } else {
                        tablediv.addClass('d-none');
                    }
                }
            });
        });
        // Add a click event listener to the table rows (including dynamically generated rows)
        tableBody.on('click', 'tr', function () {
            const usernameId = $(this).data('username-id');
            const selectedSampleIds = selectedRowIDs.join(',');
            console.log(usernameId)
            console.log(selectedSampleIds)
            // Check if the 'allow_alter' checkbox is checked
            const allowAlter = $('#allow_alter').prop('checked');
            console.log(allowAlter)

            // Perform an AJAX request to add the selected samples to the "samples_shared_with" module
            $.ajax({
                url: '/inventory/add_to_shared_inv/',
                data: {
                    'username_id': usernameId,
                    'inv_ids': selectedSampleIds,
                    'allow_alter': allowAlter  // Include the 'allow_alter' value in the request
                },
                type: 'POST',
                dataType: 'json',
                headers: { 'X-CSRFToken': getCookie('csrftoken') },
                success: function (data) {
                    if (data.success) {
                        alert("Inventory shared successfully!");
                    } else {
                        if (data.error) {
                            alert("There was a problem sharing Inventory! ERROR: " + data.error);
                            console.error(data.error);
                        }
                    }
                }
            });
        });
        // Function to retrieve the CSRF token from cookies
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Search for the CSRF token cookie
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
    });
    // Add a click event listener to the "Delete selected" link
$('.delete-selected-link').on('click', function(event) {
    event.preventDefault();  // Prevent the default link behavior (navigation)

    const selectedRowIDsString = selectedRowIDs.join(',');

// Check if any samples are selected
    if (selectedRowIDsString) {
// Perform an AJAX request to delete the selected samples
        $.ajax({
            url: 'delete_selected_samples/',
            type: 'POST',
            data: {
                'sample_ids': selectedRowIDsString,
                'csrfmiddlewaretoken': '{{ csrf_token }}',  // Include CSRF token
            },
            dataType: 'json',
            success: function(data) {
                if (data.success) {
                    alert('Selected samples deleted successfully.');
            // Reload the page or perform any other desired action
                    window.location.reload();
                } else {
                    alert('Error deleting samples.');
                }
            },
            error: function() {
                alert('Error deleting samples. Please try again later.');
            }
        });
    } else {
        alert('No samples selected for deletion.');
    }
});
});