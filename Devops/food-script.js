// Food Places JavaScript - Enhanced with Location and Smart Filtering

// Global variables
let allFoodPlaces = [];
let userLat = null;
let userLon = null;

// Load food places data
async function loadFoodPlaces() {
    try {
        const response = await fetch('food_places.json');
        const foodPlaces = await response.json();
        
        allFoodPlaces = foodPlaces;
        window.allFoodPlaces = foodPlaces; // Make globally accessible
        
        // Create filter options
        createCuisineFilters(foodPlaces);
        createBudgetFilters(foodPlaces);
        
        // Request user location
        requestUserLocation();
        
        // Display all food places initially
        displayFoodPlaces(foodPlaces);
        
        // Set up filter event listeners
        setupFilterListeners();
        
        // Update results count
        updateResultsCount(foodPlaces.length, foodPlaces.length);
        
        console.log(`Loaded ${foodPlaces.length} food places successfully!`);
        
    } catch (error) {
        console.error('Error loading food places:', error);
        document.getElementById('food-places-container').innerHTML = 
            '<p class="error-message">Error loading food places. Please try again later.</p>';
    }
}

// Request user location
function requestUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLat = position.coords.latitude;
                userLon = position.coords.longitude;
                console.log('Location obtained:', userLat, userLon);
            },
            (error) => {
                console.log('Location permission denied or unavailable');
            }
        );
    }
}

// Create cuisine type filters
function createCuisineFilters(foodPlaces) {
    const cuisineTypes = new Set();
    
    // Define more comprehensive cuisine groupings to reduce repetition
    const cuisineGroupings = {
        'Biryani & Hyderabadi': [
            'Hyderabadi Biryani', 'Hyderabadi', 'Hyderabadi / Mughlai', 'Hyderabadi / Irani cafe', 
            'Hyderabadi / Barbecue', 'Biryani / North Indian', 'Fine Dining - Hyderabadi',
            'Fine Dining - Awadhi / Hyderabadi'
        ],
        'Street Food - Chaat': [
            'Street Food / Chaat', 'Street Food / Hyderabadi'
        ],
        'Street Food - Quick Bites': [
            'Street Food', 'Street Food / Non-veg', 'Street Food / Arabian'
        ],
        'Chai & Snacks': [
            'Street Food / Tea Stall', 'Street Food / Cafe', 'Irani Cafe / Street Food',
            'Juice Center / Snacks'
        ],
        'Bakery & Sweets': [
            'Street Food / Bakery', 'Street Food / Middle Eastern', 'Casual dining / Sweets & Snacks',
            'Casual Dining / Sweets & Snacks'
        ],
        'Food Streets': [
            'Street Food / Food Street'
        ],
        'South Indian': [
            'South Indian', 'Andhra / Spicy cuisine', 'Andhra / Traditional Thali', 
            'Chettinad / South Indian', 'South Indian / Vegetarian'
        ],
        'North Indian & Mughlai': [
            'North Indian', 'Mughlai / Barbecue', 'North West Frontier', 
            'Fine Dining - North West Frontier', 'Vegetarian / North Indian'
        ],
        'Fine Dining': [
            'Fine dining / Multi-cuisine', 'Fine Dining - Indian', 'Multi-cuisine / Lounge'
        ],
        'Cafes & Bakeries': [
            'Cafe / Bakery', 'Bakery / Confectionery', 'Bakery / Hyderabadi sweets',
            'Restaurant - Multi-cuisine / Bakery'
        ],
        'Vegetarian': [
            'Vegetarian / Gujarati', 'Restaurant - Vegetarian / North Indian',
            'Restaurant - South Indian / Vegetarian'
        ],
        'Buffet & BBQ': [
            'Buffet / Barbecue', 'Restaurant - Mughlai / Barbecue'
        ],
        'Multi-Cuisine': [
            'Multi-cuisine', 'Restaurant - Multi-cuisine'
        ]
    };
    
    // Extract and group cuisine types
    foodPlaces.forEach(place => {
        if (place.place_type) {
            const cleanType = place.place_type.replace('Restaurant - ', '').trim();
            
            // Check if this type should be grouped
            let grouped = false;
            for (const [groupName, groupTypes] of Object.entries(cuisineGroupings)) {
                if (groupTypes.some(groupType => 
                    cleanType === groupType || 
                    cleanType.includes(groupType) || 
                    groupType.includes(cleanType)
                )) {
                    cuisineTypes.add(groupName);
                    grouped = true;
                    break;
                }
            }
            
            // If not grouped, add the original type (but clean it up)
            if (!grouped) {
                cuisineTypes.add(cleanType);
            }
        }
    });
    
    // Create filter checkboxes
    const container = document.getElementById('cuisine-filter-options');
    container.innerHTML = '';
    
    Array.from(cuisineTypes).sort().forEach(type => {
        const label = document.createElement('label');
        label.className = 'filter-label cuisine-filter';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'cuisine-checkbox';
        checkbox.dataset.cuisine = type;
        
        const span = document.createElement('span');
        span.textContent = type;
        
        label.appendChild(checkbox);
        label.appendChild(span);
        container.appendChild(label);
    });
}

// Create budget range filters
function createBudgetFilters(foodPlaces) {
    const budgetRanges = [
        { label: 'Budget Friendly (Under ₹200)', min: 0, max: 200 },
        { label: 'Moderate (₹200 - ₹400)', min: 200, max: 400 },
        { label: 'Premium (₹400 - ₹600)', min: 400, max: 600 },
        { label: 'Fine Dining (Above ₹600)', min: 600, max: 999999 }
    ];
    
    const container = document.getElementById('budget-filter-options');
    container.innerHTML = '';
    
    budgetRanges.forEach(range => {
        const label = document.createElement('label');
        label.className = 'filter-label budget-filter';
        
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'budget-checkbox';
        checkbox.dataset.minBudget = range.min;
        checkbox.dataset.maxBudget = range.max;
        
        const span = document.createElement('span');
        span.textContent = range.label;
        
        label.appendChild(checkbox);
        label.appendChild(span);
        container.appendChild(label);
    });
}

// Display food places as cards
function displayFoodPlaces(foodPlaces) {
    const container = document.getElementById('food-places-container');
    container.innerHTML = '';
    
    if (foodPlaces.length === 0) {
        container.innerHTML = '<p class="no-results">No food places found matching your criteria. Try adjusting your filters!</p>';
        return;
    }
    
    foodPlaces.forEach(place => {
        const card = document.createElement('div');
        card.className = 'food-place-card';
        
        card.innerHTML = `
            <div class="card-header">
                <h3 class="restaurant-name">${place.name}</h3>
                <span class="budget-badge">₹${place.max_budget_for_one}</span>
            </div>
            
            <div class="restaurant-info">
                <p class="place-type">${place.place_type}</p>
                <p class="area">${place.area}${place.specific_branch ? ' - ' + place.specific_branch : ''}</p>
                <p class="timings">${place.timings}</p>
            </div>
            
            <div class="description">
                <p>${place.description}</p>
            </div>
            
            ${place.special_dishes && place.special_dishes.length > 0 ? `
                <div class="special-dishes">
                    <h4>Must-Try Dishes</h4>
                    <div class="dishes-list">
                        ${place.special_dishes.map(dish => `<span class="dish-tag">${dish}</span>`).join('')}
                    </div>
                </div>
            ` : ''}
        `;
        
        // Add click event to expand/collapse details
        card.addEventListener('click', () => {
            card.classList.toggle('expanded');
        });
        
        container.appendChild(card);
    });
}

// Set up filter event listeners
function setupFilterListeners() {
    // Cuisine filters
    const cuisineCheckboxes = document.querySelectorAll('.cuisine-checkbox');
    cuisineCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterFoodPlaces);
    });
    
    // Budget filters
    const budgetCheckboxes = document.querySelectorAll('.budget-checkbox');
    budgetCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', filterFoodPlaces);
    });
    
    // Clear filters button
    const clearButton = document.getElementById('clear-filters');
    clearButton.addEventListener('click', () => {
        // Uncheck all checkboxes
        cuisineCheckboxes.forEach(cb => cb.checked = false);
        budgetCheckboxes.forEach(cb => cb.checked = false);
        
        // Show all food places
        displayFoodPlaces(allFoodPlaces);
        updateResultsCount(allFoodPlaces.length, allFoodPlaces.length);
    });
    
    // Show nearby button
    const nearbyButton = document.getElementById('show-nearby');
    nearbyButton.addEventListener('click', showNearbyPlaces);
}

// Filter food places based on selected criteria
function filterFoodPlaces() {
    const selectedCuisines = [];
    const selectedBudgets = [];
    
    // Get selected cuisine types
    document.querySelectorAll('.cuisine-checkbox:checked').forEach(checkbox => {
        selectedCuisines.push(checkbox.dataset.cuisine);
    });
    
    // Get selected budget ranges
    document.querySelectorAll('.budget-checkbox:checked').forEach(checkbox => {
        selectedBudgets.push({
            min: parseInt(checkbox.dataset.minBudget),
            max: parseInt(checkbox.dataset.maxBudget)
        });
    });
    
    let filteredPlaces = allFoodPlaces;
    
    // Filter by cuisine
    if (selectedCuisines.length > 0) {
        const cuisineGroupings = {
            'Biryani & Hyderabadi': [
                'Hyderabadi Biryani', 'Hyderabadi', 'Hyderabadi / Mughlai', 'Hyderabadi / Irani cafe', 
                'Hyderabadi / Barbecue', 'Biryani / North Indian', 'Fine Dining - Hyderabadi',
                'Fine Dining - Awadhi / Hyderabadi'
            ],
            'Street Food - Chaat': [
                'Street Food / Chaat', 'Street Food / Hyderabadi'
            ],
            'Street Food - Quick Bites': [
                'Street Food', 'Street Food / Non-veg', 'Street Food / Arabian'
            ],
            'Chai & Snacks': [
                'Street Food / Tea Stall', 'Street Food / Cafe', 'Irani Cafe / Street Food',
                'Juice Center / Snacks'
            ],
            'Bakery & Sweets': [
                'Street Food / Bakery', 'Street Food / Middle Eastern', 'Casual dining / Sweets & Snacks',
                'Casual Dining / Sweets & Snacks'
            ],
            'Food Streets': [
                'Street Food / Food Street'
            ],
            'South Indian': [
                'South Indian', 'Andhra / Spicy cuisine', 'Andhra / Traditional Thali', 
                'Chettinad / South Indian', 'South Indian / Vegetarian'
            ],
            'North Indian & Mughlai': [
                'North Indian', 'Mughlai / Barbecue', 'North West Frontier', 
                'Fine Dining - North West Frontier', 'Vegetarian / North Indian'
            ],
            'Fine Dining': [
                'Fine dining / Multi-cuisine', 'Fine Dining - Indian', 'Multi-cuisine / Lounge'
            ],
            'Cafes & Bakeries': [
                'Cafe / Bakery', 'Bakery / Confectionery', 'Bakery / Hyderabadi sweets',
                'Restaurant - Multi-cuisine / Bakery'
            ],
            'Vegetarian': [
                'Vegetarian / Gujarati', 'Restaurant - Vegetarian / North Indian',
                'Restaurant - South Indian / Vegetarian'
            ],
            'Buffet & BBQ': [
                'Buffet / Barbecue', 'Restaurant - Mughlai / Barbecue'
            ],
            'Multi-Cuisine': [
                'Multi-cuisine', 'Restaurant - Multi-cuisine'
            ]
        };
        
        filteredPlaces = filteredPlaces.filter(place => {
            const placeType = place.place_type.replace('Restaurant - ', '').trim();
            
            return selectedCuisines.some(selectedCuisine => {
                if (cuisineGroupings[selectedCuisine]) {
                    return cuisineGroupings[selectedCuisine].some(groupType => 
                        placeType === groupType || 
                        placeType.includes(groupType) || 
                        groupType.includes(placeType)
                    );
                } else {
                    return placeType.includes(selectedCuisine) || selectedCuisine.includes(placeType);
                }
            });
        });
    }
    
    // Filter by budget
    if (selectedBudgets.length > 0) {
        filteredPlaces = filteredPlaces.filter(place => {
            return selectedBudgets.some(budget => 
                place.max_budget_for_one >= budget.min && place.max_budget_for_one <= budget.max
            );
        });
    }
    
    // Display filtered results
    displayFoodPlaces(filteredPlaces);
    updateResultsCount(filteredPlaces.length, allFoodPlaces.length);
}

// Show nearby places (basic implementation)
function showNearbyPlaces() {
    if (!userLat || !userLon) {
        alert('Please allow location access to find nearby places!');
        return;
    }
    
    // For now, just show a message. In a real app, you'd calculate distances
    alert('Finding nearby places... (This would calculate distances to food places based on your location)');
    
    // You could implement distance calculation here similar to the tourist places page
    // For demonstration, let's just show the first 10 places
    const nearbyPlaces = allFoodPlaces.slice(0, 10);
    displayFoodPlaces(nearbyPlaces);
    updateResultsCount(nearbyPlaces.length, allFoodPlaces.length);
}

// Update results count display
function updateResultsCount(filtered, total) {
    const countElement = document.getElementById('results-count');
    countElement.textContent = `Showing ${filtered} of ${total} food places`;
}

// Load food places when page loads
document.addEventListener('DOMContentLoaded', loadFoodPlaces);