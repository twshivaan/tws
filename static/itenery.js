const rightBtn = document.querySelector('#right-button');
const leftBtn = document.querySelector('#left-button');

rightBtn.addEventListener("click", function(event) {
  const conent = document.querySelector('#content');
  conent.scrollLeft += 300;
  event.preventDefault();
});

leftBtn.addEventListener("click", function(event) {
  const conent = document.querySelector('#content');
  conent.scrollLeft -= 300;
  event.preventDefault();
});


// JavaScript for the lightbox

const attractions = document.querySelectorAll('.attraction');
const lightbox = document.getElementById('lightbox');
const lightboxContent = document.querySelector('.lightbox-content');

attractions.forEach(attraction => {
    attraction.addEventListener('click', function () {
        const attractionName = attraction.querySelector('.attractionName').textContent;
        const attractionLocation = attraction.querySelector('.attractionLocation').textContent;
        const attractionRating = attraction.querySelector('.attractionRating').textContent;
        const attractionTimings = JSON.parse(attraction.querySelector('.attractionTiming').textContent);
        const attractionDuration = attraction.querySelector('.attractionDuration').textContent;
        const attractionAbout = attraction.querySelector('.attractionAbout').textContent;
        const attractionPhotos = JSON.parse(attraction.querySelector('.attractionPhotos').textContent);


        // Create an image element
        const imageUrl = attractionPhotos[Math.floor(Math.random() * 5)];
        const image = document.createElement('img');
        // Set the src attribute of the image element
        image.src = imageUrl;
        image.classList.add('banner-image');
        // Append the image element to the div with id "image-container"
        const banner = document.getElementById('lightbox-banner');
        banner.appendChild(image);


        // Populate the lightbox elements with attraction details
        document.getElementById('lightbox-name').textContent = attractionName;
        document.getElementById('lightbox-duration').textContent = attractionDuration;
        document.getElementById('lightbox-location').innerHTML = attractionLocation;
        document.getElementById('lightbox-rating').textContent = attractionRating;
        
        const tbody = document.getElementById("lightbox-timing");
        const headingRow = document.createElement("tr");
        headingRow.innerHTML = `
            <th class = "heading">Timings :</th>
        `;
        tbody.appendChild(headingRow);
        for (const key in attractionTimings) {
            if (attractionTimings.hasOwnProperty(key)) {
                const dayData = attractionTimings[key];
                const row = document.createElement("tr");
                if (dayData.open == 'Open'){
                    row.innerHTML = `
                        <td>${dayData.day}</td>
                        <td>${dayData.opening_time}</td>
                        <td>-</td>
                        <td>${dayData.closing_time}</td>
                    `;
                }
                else{
                    row.innerHTML = `
                        <td>${dayData.day}</td>
                        <td>${dayData.open}</td>
                    `;
                }
                tbody.appendChild(row);
            }
        }

        const durationValue = document.getElementById('lightbox-duration');
        const decrementButton = document.getElementById('decrement-duration');
        const incrementButton = document.getElementById('increment-duration');
        let currentDuration = parseInt(durationValue.textContent);
        const attractionDurationDiv = attraction.querySelector('.attractionDuration');

        function updateDuration() {
            console.log(attraction.id)
            durationValue.textContent = currentDuration;
            attractionDurationDiv.textContent = currentDuration;
        }
        updateDuration();
        // Decrement the duration when the "-" button is clicked
        decrementButton.addEventListener('click', function () {
            if (currentDuration > 1) {
                currentDuration -= 1; // You can change the decrement value as needed
                updateDuration();
            }
        });

        // Increment the duration when the "+" button is clicked
        incrementButton.addEventListener('click', function () {
            if (currentDuration < 9) {
                currentDuration += 1; // You can change the decrement value as needed
                updateDuration();
            }
        });

        let currentIndex = 0;
        const lightboxPhotos = document.getElementById("lightbox-photos");
        const attractionImage = document.createElement('img');
        // Set the src attribute of the image element
        attractionImage.src = attractionPhotos[currentIndex];
        attractionImage.classList.add('lightbox-image');
        lightboxPhotos.appendChild(attractionImage);

        // Function to change the displayed image
        function changeImage() {
            currentIndex+=1;
            currentIndex%=attractionPhotos.length;
            attractionImage.src = attractionPhotos[currentIndex];
        }

        attractionImage.addEventListener("click", () => {
            changeImage();
        });



        document.getElementById('lightbox-about').textContent = attractionAbout;

        // Get the button element and the attractionRemove element
        const removeButton = document.getElementById("lightbox-remove");
        const attractionRemove = attraction.querySelector(".attractionRemove");

        if(attractionRemove.textContent === "1"){
            removeButton.textContent = "Removed";
        }

        // Add a click event listener to the button
        removeButton.addEventListener("click", function () {
            // Toggle the value of the attractionRemove element
            if (attractionRemove.textContent === "0") {
                attractionRemove.textContent = "1";
            }
            removeButton.textContent = "Removed";
        });


        lightbox.style.display = 'block';

        // Attach a click event handler to the close button
        const closeButton = document.querySelector('.close-button');
        closeButton.addEventListener('click', function () {
            tbody.innerHTML = '';
            banner.innerHTML = '';
            lightboxPhotos.innerHTML = '';
            removeButton.textContent = "Remove";
            lightbox.style.display = 'none';
        });
    },false);
});

window.addEventListener('click', function (event) {
    if (event.target === lightbox) {
        const tbody = document.getElementById("lightbox-timing");
        const banner = document.getElementById('lightbox-banner');
        const lightboxPhotos = document.getElementById("lightbox-photos");
        const removeButton = document.getElementById("lightbox-remove");
        banner.innerHTML = '';
        tbody.innerHTML = '';
        lightboxPhotos.innerHTML = '';
        removeButton.textContent = 'Remove';
        lightbox.style.display = 'none';
    }
});


// ADD PLACE
const addPlaceButton = document.querySelector('#add-place-button');
const addPlaceLightbox = document.getElementById('add-place-lightbox');
const closeButton = document.querySelector('#add-place-lightbox .close-button');
const addPlaceSubmitButton = document.querySelector('#add-place-submit');

function openAddPlaceLightbox() {
    addPlaceLightbox.style.display = 'block';
}

function closeAddPlaceLightbox() {
    addPlaceLightbox.style.display = 'none';
}

addPlaceButton.addEventListener('click', openAddPlaceLightbox);
closeButton.addEventListener('click', closeAddPlaceLightbox);

window.addEventListener('click', function (event) {
    if (event.target === addPlaceLightbox) {
        closeAddPlaceLightbox();
    }
});

addPlaceSubmitButton.addEventListener('click', function () {
    const placeName = document.getElementById('place-name').value;
    closeAddPlaceLightbox();
});



//EDIT TYPE
// Function to open the Edit Place lightbox
function openEditPlaceLightbox() {
    document.getElementById('edit-place-lightbox').style.display = 'block';
}

// Function to close the Edit Place lightbox
function closeEditPlaceLightbox() {
    document.getElementById('edit-place-lightbox').style.display = 'none';
}

// Event listener to open the Edit Place lightbox when the Edit Place button is clicked
document.getElementById('edit-place-button').addEventListener('click', openEditPlaceLightbox);

// Event listener to close the Edit Place lightbox when the close button is clicked
document.querySelector('.close-button').addEventListener('click',function() {
    // Check if any attraction type buttons are selected
    const selectedButtons = document.querySelectorAll('.attraction-type-button.selected');
    if (selectedButtons.length === 0) {
        alert('Please select at least some types.');
    } else {
        // Save changes logic here
        // ...

        // Close the Edit Place lightbox
        closeEditPlaceLightbox();
    }
});

// Event listener to close the Edit Place lightbox when the close button is clicked
document.getElementById('edit-place-submit').addEventListener('click',function() {
    // Check if any attraction type buttons are selected
    const selectedButtons = document.querySelectorAll('.attraction-type-button.selected');
    if (selectedButtons.length === 0) {
        alert('Please select at least some types.');
    } else {
        // Save changes logic here
        // ...

        // Close the Edit Place lightbox
        closeEditPlaceLightbox();
    }
});

const attractionButtons = document.querySelectorAll(".attraction-type-button");
const selectedAttractionsInput = document.getElementById("selected-attractions");
const selectAllButton = document.getElementById("select-all");
const clearAllButton = document.getElementById("clear-all");

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
function updateSelectedAttractions() {
    const selectedAttractions = Array.from(attractionButtons)
        .filter(button => button.classList.contains("selected"))
        .map(button => button.getAttribute("data-attraction"));

    selectedAttractionsInput.value = JSON.stringify(selectedAttractions);
}

const filterButton = document.getElementById("filter-button");

filterButton.addEventListener("click", function () {
    const city = filterButton.getAttribute("data-city-name");
    const startDate = filterButton.getAttribute("data-start-date");
    const endDate = filterButton.getAttribute("data-end-date");

    // Get all elements with the "attraction-type-button" class
    const attractionTypeButtons = document.querySelectorAll('.attraction-type-button');
    const selectedAttractionTypeButtons = [];
    attractionTypeButtons.forEach((button) => {
        if (button.classList.contains('selected')) {
            selectedAttractionTypeButtons.push(button.textContent.trim());
        }
    });

    // Get all elements with the class "attraction"
    const attractionElements = document.querySelectorAll('.attraction');
    const idsToRemove = [];
    const idsWithDurationChange = [];
    const newDurations = [];

    attractionElements.forEach((attractionElement) => {
        const id = attractionElement.id.replace('attractionID-', '');

        const attractionRemove = attractionElement.querySelector('.attractionRemove').textContent;
        if (attractionRemove === '1') {
            idsToRemove.push(parseInt(id));
        }

        const oldDuration = attractionElement.querySelector('.attractionInitDuration').textContent;
        const newDuration = attractionElement.querySelector('.attractionDuration').textContent;
        if (oldDuration!=newDuration){
            idsWithDurationChange.push(parseInt(id));
            newDurations.push(parseInt(newDuration));    
        }

    });

    const dur = [idsWithDurationChange, newDurations];
    
    const request = {
        city: city,
        st_date: startDate,
        en_date: endDate,
        types: selectedAttractionTypeButtons,
        exclude: idsToRemove,
        include: [],
        duration: dur
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