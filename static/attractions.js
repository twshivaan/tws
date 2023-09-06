document.addEventListener("DOMContentLoaded", function () {
    const attractionButtons = document.querySelectorAll(".attraction-type-button");
    const selectedAttractionsInput = document.getElementById("selected-attractions");
    const selectAllButton = document.getElementById("select-all");
    const clearAllButton = document.getElementById("clear-all");
    const locationIcon = document.getElementById("location-icon-attraction");

    // Extract city_name, start_date, and end_date from data attributes
    const city = locationIcon.getAttribute("data-city-name");
    const startDate = locationIcon.getAttribute("data-start-date");
    const endDate = locationIcon.getAttribute("data-end-date");

    // Handle attraction type buttons
    attractionButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            this.classList.toggle("selected");
            updateSelectedAttractions();
        });
    });

    // Handle "Select All" button
    selectAllButton.addEventListener("click", function () {
        attractionButtons.forEach(function (button) {
            button.classList.add("selected");
        });
        this.classList.toggle("active"); // Toggle the class to change color
        updateSelectedAttractions();
    });

    // Handle "Clear All" button
    clearAllButton.addEventListener("click", function () {
        attractionButtons.forEach(function (button) {
            button.classList.remove("selected");
        });
        selectAllButton.classList.remove("active"); // Remove the class to reset color
        updateSelectedAttractions();
    });

    // Handle location icon click
    locationIcon.addEventListener("click", function () {
        // Move this line after the variable declaration
        const selectedAttractionsInputValue = JSON.parse(selectedAttractionsInput.value);

        console.log(selectedAttractionsInputValue);

        if (selectedAttractionsInputValue.length === 0) {
            alert("Please select at least one attraction.");
            event.preventDefault();
        }

        const request = {
            city: city,
            st_date: startDate,
            en_date: endDate,
            types: selectedAttractionsInputValue,
            exclude: [],
            include: [],
            duration: [[], []]
        };

        fetch('/itenery', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(request)
        }).then(response => {
            if (response.ok) {
                console.log('ok')
                window.location.href = `/itenery`;
            } else {
                console.error('Error:', response.statusText);
            }
            // Handle the response if needed
            console.log(response);
        }).catch(error => {
            // Handle errors if needed
            console.error(error);
        });
    });

    function updateSelectedAttractions() {
        const selectedAttractions = Array.from(attractionButtons)
            .filter(button => button.classList.contains("selected"))
            .map(button => button.getAttribute("data-attraction"));

        selectedAttractionsInput.value = JSON.stringify(selectedAttractions);
    }
});

