// Fetch road distance from OSRM
async function getRoadDistance(userLat, userLon, destLat, destLon) {
    const url = `https://router.project-osrm.org/route/v1/driving/${userLon},${userLat};${destLon},${destLat}?overview=false`;
    try {
        const response = await fetch(url);
        const data = await response.json();
        if (data.routes && data.routes.length > 0) {
            return (data.routes[0].distance / 1000).toFixed(2); // km
        }
        return "N/A";
    } catch (err) {
        console.error('Error fetching road distance:', err);
        return "N/A";
    }
}

// Display destinations as cards
function displayDestinations(destinations, userLat = null, userLon = null) {
    const container = document.getElementById('destinations-container');
    container.innerHTML = '';

    if (destinations.length === 0) {
        container.innerHTML = '<p class="no-results">No destinations found matching the selected filters.</p>';
        return;
    }

    destinations.forEach(destination => {
        const destDiv = document.createElement('div');
        destDiv.className = 'destination-card';
        destDiv.id = `dest-${destination.name.replace(/\s+/g,'')}`;

        const distanceText = destination.user_distance ? destination.user_distance + ' km' : 'N/A';
        destDiv.innerHTML = `
            <h3 class="destination-name">${destination.name}</h3>
            <div class="destination-info">
                <p class="place-type"><strong>Type:</strong> ${destination.place_type}</p>
                <p class="distance"><strong>Distance from you:</strong> <span class="distance-value">${distanceText}</span></p>
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
                </div>` : ''}
            <button class="calc-distance-btn">Get Distance</button>
        `;

        // Toggle expanded card on click
        destDiv.addEventListener('click', (e) => {
            if(!e.target.classList.contains('calc-distance-btn')) {
                destDiv.classList.toggle('expanded');
            }
        });

        // Button to calculate distance individually
        const btn = destDiv.querySelector('.calc-distance-btn');
        btn.addEventListener('click', async () => {
            if(userLat && userLon && destination.latitude && destination.longitude) {
                btn.disabled = true;
                btn.textContent = 'Calculating...';
                const dist = await getRoadDistance(userLat, userLon, destination.latitude, destination.longitude);
                destination.user_distance = dist;
                destDiv.querySelector('.distance-value').textContent = dist + ' km';
                btn.textContent = 'Get Distance';
                btn.disabled = false;
            }
        });

        container.appendChild(destDiv);
    });
}

// Extract unique types and create filter checkboxes
function createFilterOptions(destinations) {
    const uniqueTypes = new Set();
    
    // Define type groupings to reduce clutter
    const typeGroupings = {
        'Parks': ['Amusement Park', 'Amusement & Water Park', 'Amusement & Theme Park', 'Winter Park', 'Zoological Park', 'Botanical Garden', 'Park', 'Lake Front & Park'],
        'Heritage': ['Heritage', 'Monument', 'Fort', 'Palace', 'Tomb'],
        'Museums': ['Museum', 'Art', 'Antiques'],
        'Religious': ['Hindu Temple'],
        'Entertainment': ['Film Studio', 'Planetarium', 'Space Shows'],
        'Nature': ['Lake Front', 'Scenic Drive'],
        'Shopping': ['Shopping'],
        'Hotels': ['Hotel']
    };
    
    destinations.forEach(dest => {
        if(dest.place_type) {
            const types = dest.place_type.split(',').map(t => t.trim());
            types.forEach(type => {
                // Check if this type should be grouped
                let grouped = false;
                for (const [groupName, groupTypes] of Object.entries(typeGroupings)) {
                    if (groupTypes.includes(type)) {
                        uniqueTypes.add(groupName);
                        grouped = true;
                        break;
                    }
                }
                // If not grouped, add the original type
                if (!grouped) {
                    uniqueTypes.add(type);
                }
            });
        }
    });

    const sortedTypes = Array.from(uniqueTypes).sort();
    const filterContainer = document.getElementById('filter-options');
    filterContainer.innerHTML = '';

    sortedTypes.forEach(type => {
        const label = document.createElement('label');
        label.className = 'filter-label';
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'filter-checkbox';
        checkbox.dataset.type = type;
        const span = document.createElement('span');
        span.textContent = type;
        label.appendChild(checkbox);
        label.appendChild(span);
        filterContainer.appendChild(label);
    });
}

// Create budget filter options
function createBudgetFilterOptions(destinations) {
    const budgetRanges = [
        { label: 'Free', min: 0, max: 0 },
        { label: 'Under ₹50', min: 1, max: 50 },
        { label: '₹50 - ₹200', min: 50, max: 200 },
        { label: '₹200 - ₹500', min: 200, max: 500 },
        { label: '₹500 - ₹1000', min: 500, max: 1000 },
        { label: 'Above ₹1000', min: 1000, max: Infinity }
    ];

    const filterContainer = document.getElementById('budget-filter-options');
    filterContainer.innerHTML = '';

    budgetRanges.forEach(range => {
        const label = document.createElement('label');
        label.className = 'filter-label';
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.className = 'budget-filter-checkbox';
        checkbox.dataset.min = range.min;
        checkbox.dataset.max = range.max;
        const span = document.createElement('span');
        span.textContent = range.label;
        label.appendChild(checkbox);
        label.appendChild(span);
        filterContainer.appendChild(label);
    });
}

// Extract numeric value from entry fee string
function extractEntryFee(entryFeeString) {
    if (!entryFeeString) return null;
    
    // Handle "Free" entries
    if (entryFeeString.toLowerCase().includes('free')) return 0;
    
    // Extract first numeric value (usually for Indians/Adults)
    const match = entryFeeString.match(/₹(\d+)/);
    return match ? parseInt(match[1]) : null;
}

// Filter destinations
function filterDestinations() {
    const selectedTypes = Array.from(document.querySelectorAll('.filter-checkbox:checked')).map(cb => cb.dataset.type);
    const selectedBudgetRanges = Array.from(document.querySelectorAll('.budget-filter-checkbox:checked')).map(cb => ({
        min: parseInt(cb.dataset.min),
        max: parseInt(cb.dataset.max)
    }));

    let filtered;
    if(selectedTypes.length === 0 && selectedBudgetRanges.length === 0) {
        filtered = window.allDestinations;
    } else {
        // Define type groupings (same as in createFilterOptions)
        const typeGroupings = {
            'Parks': ['Amusement Park', 'Amusement & Water Park', 'Amusement & Theme Park', 'Winter Park', 'Zoological Park', 'Botanical Garden', 'Park', 'Lake Front & Park'],
            'Heritage': ['Heritage', 'Monument', 'Fort', 'Palace', 'Tomb'],
            'Museums': ['Museum', 'Art', 'Antiques'],
            'Religious': ['Hindu Temple'],
            'Entertainment': ['Film Studio', 'Planetarium', 'Space Shows'],
            'Nature': ['Lake Front', 'Scenic Drive'],
            'Shopping': ['Shopping'],
            'Hotels': ['Hotel']
        };
        
        filtered = window.allDestinations.filter(dest => {
            // Type filter
            let typeMatch = selectedTypes.length === 0; // If no types selected, pass type filter
            if (selectedTypes.length > 0 && dest.place_type) {
                const types = dest.place_type.split(',').map(t => t.trim());
                
                typeMatch = selectedTypes.some(selectedType => {
                    // If the selected type is a group, check if any destination type belongs to that group
                    if (typeGroupings[selectedType]) {
                        return types.some(destType => 
                            typeGroupings[selectedType].includes(destType)
                        );
                    } else {
                        // If it's not a group, check direct match
                        return types.includes(selectedType);
                    }
                });
            }
            
            // Budget filter
            let budgetMatch = selectedBudgetRanges.length === 0; // If no budget selected, pass budget filter
            if (selectedBudgetRanges.length > 0) {
                const entryFee = extractEntryFee(dest.entry_fee);
                if (entryFee !== null) {
                    budgetMatch = selectedBudgetRanges.some(range => {
                        if (range.max === Infinity) {
                            return entryFee >= range.min;
                        } else {
                            return entryFee >= range.min && entryFee <= range.max;
                        }
                    });
                }
            }
            
            return typeMatch && budgetMatch;
        });
    }

    displayDestinations(filtered, window.userLat, window.userLon);
    updateFilterCount(filtered.length, window.allDestinations.length);
}

// Filter count display
function updateFilterCount(filtered, total) {
    const filterContainer = document.getElementById('filter-container');
    let countDisplay = filterContainer.querySelector('.filter-count');
    if(!countDisplay) {
        countDisplay = document.createElement('p');
        countDisplay.className = 'filter-count';
        filterContainer.appendChild(countDisplay);
    }
    countDisplay.textContent = `Showing ${filtered} of ${total} destinations`;
}

// Setup filter listeners
function setupFilterListeners() {
    const filterCheckboxes = document.querySelectorAll('.filter-checkbox');
    filterCheckboxes.forEach(cb => cb.addEventListener('change', filterDestinations));
    
    const budgetFilterCheckboxes = document.querySelectorAll('.budget-filter-checkbox');
    budgetFilterCheckboxes.forEach(cb => cb.addEventListener('change', filterDestinations));

    const clearButton = document.getElementById('clear-filters');
    if(clearButton) {
        clearButton.addEventListener('click', () => {
            filterCheckboxes.forEach(cb => cb.checked = false);
            budgetFilterCheckboxes.forEach(cb => cb.checked = false);
            displayDestinations(window.allDestinations, window.userLat, window.userLon);
        });
    }
}

// Sort by nearest (top 5)
// Optimized: Fetch top 5 nearest places faster using parallel requests
function getHaversine(lat1, lon1, lat2, lon2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLon = (lon2 - lon1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLon/2)**2;
  return (R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))).toFixed(2);
}

async function showNearestPlaces() {
  if(!window.userLat || !window.userLon) {
    alert("Please allow location access first.");
    return;
  }

  const spinner = document.getElementById('loading-spinner');
  spinner.style.display = 'block';

  // Step 1: local distance estimation
  window.allDestinations.forEach(dest => {
    if(dest.latitude && dest.longitude) {
      dest.user_distance = getHaversine(window.userLat, window.userLon, dest.latitude, dest.longitude);
    }
  });

  // Step 2: sort by approximate distance and pick top 5
  const top5 = window.allDestinations
    .filter(d => d.user_distance !== "N/A")
    .sort((a,b) => parseFloat(a.user_distance) - parseFloat(b.user_distance))
    .slice(0,5);

  // Step 3: refine these 5 with OSRM
  for (const dest of top5) {
    dest.user_distance = await getRoadDistance(window.userLat, window.userLon, dest.latitude, dest.longitude);
    await new Promise(r => setTimeout(r, 500)); // light delay
  }

  displayDestinations(top5, window.userLat, window.userLon);
  spinner.style.display = 'none';
}

// Load destinations
async function loadDestinations() {
    try {
        const response = await fetch('data.json');
        const destinations = await response.json();
        window.allDestinations = destinations;

        createFilterOptions(destinations);
        createBudgetFilterOptions(destinations);

        if(navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(pos => {
                window.userLat = pos.coords.latitude;
                window.userLon = pos.coords.longitude;
                displayDestinations(destinations, window.userLat, window.userLon);
                setupFilterListeners();
            }, err => {
                alert("Location permission denied. Distances will not be available.");
                displayDestinations(destinations);
                setupFilterListeners();
            });
        } else {
            alert("Geolocation not supported.");
            displayDestinations(destinations);
            setupFilterListeners();
        }

        // Optional: Add nearest filter button dynamically
        const filterContainer = document.getElementById('filter-container');
        const nearestBtn = document.createElement('button');
        nearestBtn.textContent = 'Show Nearest 5 Places';
        nearestBtn.style.background = '#007bff';
        nearestBtn.style.color = 'white';
        nearestBtn.style.border = 'none';
        nearestBtn.style.padding = '0.7rem 1.2rem';
        nearestBtn.style.borderRadius = '8px';
        nearestBtn.style.marginLeft = '1rem';
        nearestBtn.style.cursor = 'pointer';
        nearestBtn.addEventListener('click', showNearestPlaces);
        filterContainer.appendChild(nearestBtn);

    } catch(err) {
        console.error('Error loading destinations:', err);
        document.getElementById('destinations-container').innerHTML =
            '<p class="error-message">Error loading destinations. Please try again later.</p>';
    }
}

document.addEventListener('DOMContentLoaded', loadDestinations);
