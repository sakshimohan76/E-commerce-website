
var fullImgBox = document.getElementById("fullImgBox");
var fullImg = document.getElementById("fullImg");

function openFullImg(pic) {
    fullImgBox.style.display = "flex";
    fullImg.src = pic;
}

function closeFullImg() {
    fullImgBox.style.display = "none";
}


// Get references to the search input and search results container
const searchInput = document.getElementById('searchInput');
const searchResults = document.getElementById('searchResults');
const container = document.querySelector('.container'); // Container for all cards

// Function to perform the search
const performSearch = () => {
    const searchTerm = searchInput.value.toLowerCase().trim(); // Convert input to lowercase for case-insensitive search
    const cards = Array.from(container.querySelectorAll('.card')); // Get all cards

    searchResults.innerHTML = ''; // Clear previous search results

    if (searchTerm === '') {
        cards.forEach(card => {
            card.style.display = 'block'; // Show all cards when search input is empty
        });
        return;
    }

    cards.forEach(card => {
        const cardTitle = card.querySelector('.card-title').textContent.toLowerCase();
        const cardDesc = card.querySelector('.card-text').textContent.toLowerCase();
        if (cardTitle.includes(searchTerm) || cardDesc.includes(searchTerm)) {
            card.style.display = 'block'; // Show matching card
            searchResults.appendChild(card.cloneNode(true)); // Append matching card to search results
        }
    });

    if (searchResults.children.length === 0) {
        searchResults.innerHTML = '<p>No results found.</p>';
    }
};

// Attach the search function to the input's input event
searchInput.addEventListener('input', performSearch);