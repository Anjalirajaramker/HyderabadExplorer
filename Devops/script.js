// Fetch and display destination data with dynamic filtering
async function loadDestinations() {
    try {
        // Fetch the data.json file
        const response = await fetch('data.json');
        const destinations = await response.json();
        
        // Store original data globally for filtering
        window.allDestinations = destinations;
        
        // Extract and create filter options
        createFilterOptions(destinations);
        
        // Display all destinations initially
        displayDestinations(destinations);
        
        // Set up filter event listeners
        setupFilterListeners();
        
        console.log(`Loaded ${destinations.length} destinations successfully!`);
        
    } catch (error) {
        console.error('Error loading destinations:', error);
        
        // Display error message to user
        const container = document.getElementById('destinations-container');
        container.innerHTML = '<p class="error-message">Error loading destinations. Please try again later.</p>';
    }
}

// Extract unique place types from the data and create filter checkboxes
function createFilterOptions(destinations) {
    const uniqueTypes = new Set();
    
    // Extract all place types (they are comma-separated in the data)
    destinations.forEach(destination => {
        if (destination.place_type) {
            // Split by comma and clean up each type
            const types = destination.place_type.split(',').map(type => type.trim());
            types.forEach(type => uniqueTypes.add(type));
        }
    });
    
    // Sort the types alphabetically
    const sortedTypes = Array.from(uniqueTypes).sort();
    
    // Create filter checkboxes
    const filterContainer = document.getElementById('filter-options');
    filterContainer.innerHTML = '';
    
    sortedTypes.forEach(type => {
        const label = document.createElement('label');
        label.className = 'filter-label';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'filter-checkbox';
        checkbox.value = type;
        checkbox.dataset.type = type;
        
        const span = document.createElement('span');
        span.textContent = type;
        
        label.appendChild(checkbox);
        label.appendChild(span);
        filterContainer.appendChild(label);
    });
}

// Display destinations as cards
function displayDestinations(destinations) {
    const container = document.getElementById('destinations-container');
    container.innerHTML = '';
    
    if (destinations.length === 0) {
        container.innerHTML = '<p class="no-results">No destinations found matching the selected filters.</p>';
        return;
    }
    
    destinations.forEach(destination => {
        // Create destination card
        const destinationDiv = document.createElement('div');
        destinationDiv.className = 'destination-card';
        
        // Create card content
        destinationDiv.innerHTML = `
            <h3 class="destination-name">${destination.name}</h3>
            <div class="destination-info">
                <p class="place-type"><strong>Type:</strong> ${destination.place_type}</p>
                <p class="distance"><strong>Distance:</strong> ${destination.distance_from_city}</p>
                <p class="ideal-for"><strong>Ideal for:</strong> ${destination.ideal_for}</p>
                <p class="timings"><strong>Timings:</strong> ${destination.timings}</p>
                <p class="entry-fee"><strong>Entry Fee:</strong> ${destination.entry_fee}</p>
            </div>
            <div class="description">
                <p>${destination.description.substring(0, 200)}${destination.description.length > 200 ? '...' : ''}</p>
            </div>
            ${destination.food_places_near && destination.food_places_near.length > 0 ? `
                <div class="food-places">
                    <h4>🍽️ Food Places Nearby:</h4>
                    <ul>
                        ${destination.food_places_near.map(place => `<li>${place}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        `;
        
        // Add click event to expand/collapse details
        destinationDiv.addEventListener('click', () => {
            destinationDiv.classList.toggle('expanded');
        });
        
        container.appendChild(destinationDiv);
    });
}

// Set up event listeners for filters
function setupFilterListeners() {
    // Filter checkboxes
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox');
    filterCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterDestinations);
    });
    
    // Clear filters button
    const clearButton = document.getElementById('clear-filters');
    clearButton.addEventListener('click', () => {
        // Uncheck all checkboxes
        filterCheckboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        // Show all destinations
        displayDestinations(window.allDestinations);
    });
}

// Filter destinations based on selected types
function filterDestinations() {
    const selectedTypes = [];
    
    // Get all checked filter types
    document.querySelectorAll('.filter-checkbox:checked').forEach(checkbox => {
        selectedTypes.push(checkbox.dataset.type);
    });
    
    let filteredDestinations;
    
    if (selectedTypes.length === 0) {
        // No filters selected, show all destinations
        filteredDestinations = window.allDestinations;
    } else {
        // Filter destinations that match any of the selected types
        filteredDestinations = window.allDestinations.filter(destination => {
            if (!destination.place_type) return false;
            
            // Check if any of the destination's types match the selected filters
            const destinationTypes = destination.place_type.split(',').map(type => type.trim());
            return selectedTypes.some(selectedType => 
                destinationTypes.includes(selectedType)
            );
        });
    }
    
    // Display filtered results
    displayDestinations(filteredDestinations);
    
    // Update filter count display
    updateFilterCount(filteredDestinations.length, window.allDestinations.length);
}

// Update filter count display
function updateFilterCount(filtered, total) {
    const filterContainer = document.getElementById('filter-container');
    let countDisplay = filterContainer.querySelector('.filter-count');
    
    if (!countDisplay) {
        countDisplay = document.createElement('p');
        countDisplay.className = 'filter-count';
        filterContainer.appendChild(countDisplay);
    }
    
    countDisplay.textContent = `Showing ${filtered} of ${total} destinations`;
}

// Load destinations when the page loads
document.addEventListener('DOMContentLoaded', loadDestinations);