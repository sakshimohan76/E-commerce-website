
const fullImgBox = document.getElementById("fullImgBox");
const fullImg = document.getElementById("fullImg");
const header = document.querySelector(".nav");

function openFullImg(pic) {
    fullImgBox.style.display = "flex";
    fullImg.src = pic;
}

function closeFullImg() {
    fullImgBox.style.display = "none";
}

window.addEventListener('scroll', () => {
    const scrolledAmount = window.scrollY;
    const headerClassList = header.classList;
    if(scrolledAmount > 100 && !headerClassList.contains("scrolledNav")) {
        header.classList.add("scrolledNav")
    } else if(scrolledAmount < 100 && headerClassList.contains("scrolledNav")) {
        header.classList.remove("scrolledNav")
    }
})


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
        searchResults.style.display = 'none';
        return;
    } else {
        searchResults.style.display = 'flex';
    }

    cards.forEach(card => {
        const cardTitle = card.querySelector('.card-title').textContent.toLowerCase();
        const cardDesc = card.querySelector('.card-text').textContent.toLowerCase();
        if (cardTitle.includes(searchTerm) || cardDesc.includes(searchTerm)) {
            card.style.display = 'flex'; // Show matching card
            searchResults.appendChild(card.cloneNode(true)); // Append matching card to search results
        }
    });
    lazyLoadImages(searchResults);

    if (searchResults.children.length === 0) {
        searchResults.innerHTML = '<p>No results found.</p>';
    }
};

// Attach the search function to the input's input event
searchInput.addEventListener('input', performSearch);