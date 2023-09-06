// script.js

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("location-icon").addEventListener("click", function () {
        const selectedCity = document.getElementById("selected-city").value;
        const startDate = document.getElementById("start-date").value;
        const endDate = document.getElementById("end-date").value;

        if (selectedCity && startDate && endDate) {
            if (endDate < startDate) {
                alert("End date must be after start date.");
                return;
            }
            const data = JSON.stringify({
                city: selectedCity,
                startDate: startDate,
                endDate: endDate
            });
            fetch(`/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `data=${encodeURIComponent(data)}`
            }).then(response => {
                if (response.ok) {
                    window.location.href = `/select_attractions/`;
                } else {
                    console.error('Error:', response.statusText);
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        } else { 
            alert("Please fill in all fields.");
        }
    });

});
