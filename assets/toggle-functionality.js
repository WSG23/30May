// assets/toggle-functionality.js
// Modern Toggle Switch Functionality

document.addEventListener('DOMContentLoaded', function() {
    console.log('Toggle functionality loaded');
    initializeToggleSwitches();
});

// Initialize toggle switch functionality
function initializeToggleSwitches() {
    // Find all toggle containers
    const toggleContainers = document.querySelectorAll('.toggle-container');
    
    toggleContainers.forEach(container => {
        setupToggleSwitch(container);
    });
}

// Setup individual toggle switch
function setupToggleSwitch(container) {
    const toggleSwitch = container.querySelector('.toggle-switch');
    const leftLabel = container.querySelector('.toggle-label-left');
    const rightLabel = container.querySelector('.toggle-label-right');
    
    if (!toggleSwitch) return;
    
    // Find the associated hidden radio buttons
    const radioItems = findAssociatedRadioItems(container);
    
    if (!radioItems) {
        console.warn('No associated radio items found for toggle switch');
        return;
    }
    
    // Set initial state based on radio button value
    updateToggleVisualState(container, radioItems.value === 'yes');
    
    // Add click event listener
    container.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        // Toggle the state
        const isCurrentlyActive = toggleSwitch.classList.contains('active');
        const newValue = isCurrentlyActive ? 'no' : 'yes';
        
        // Update the hidden radio button
        updateRadioValue(radioItems, newValue);
        
        // Update visual state
        updateToggleVisualState(container, newValue === 'yes');
        
        // Trigger change event for Dash callbacks
        triggerDashCallback(radioItems);
    });
    
    // Watch for external changes to radio buttons (from Dash)
    observeRadioChanges(radioItems, container);
}

// Find the associated radio items for a toggle container
function findAssociatedRadioItems(container) {
    // Look for radio items in the same parent or nearby
    let parent = container.parentElement;
    while (parent && !parent.querySelector('input[type="radio"]')) {
        parent = parent.parentElement;
        if (parent === document.body) break;
    }
    
    const radioContainer = parent ? parent.querySelector('[id*="manual-map-toggle"]') : null;
    return radioContainer;
}

// Update toggle visual state
function updateToggleVisualState(container, isActive) {
    const toggleSwitch = container.querySelector('.toggle-switch');
    const leftLabel = container.querySelector('.toggle-label-left');
    const rightLabel = container.querySelector('.toggle-label-right');
    
    if (isActive) {
        toggleSwitch.classList.add('active');
        leftLabel.classList.remove('active');
        rightLabel.classList.add('active');
    } else {
        toggleSwitch.classList.remove('active');
        leftLabel.classList.add('active');
        rightLabel.classList.remove('active');
    }
}

// Update radio button value
function updateRadioValue(radioContainer, value) {
    const radioInputs = radioContainer.querySelectorAll('input[type="radio"]');
    
    radioInputs.forEach(input => {
        if (input.value === value) {
            input.checked = true;
        } else {
            input.checked = false;
        }
    });
}

// Trigger Dash callback by dispatching change event
function triggerDashCallback(radioContainer) {
    const checkedRadio = radioContainer.querySelector('input[type="radio"]:checked');
    if (checkedRadio) {
        // Create and dispatch change event
        const event = new Event('change', { bubbles: true });
        checkedRadio.dispatchEvent(event);
        
        // Also try dispatching on the container (for Dash)
        const containerEvent = new Event('change', { bubbles: true });
        radioContainer.dispatchEvent(containerEvent);
    }
}

// Observe radio button changes from external sources (Dash callbacks)
function observeRadioChanges(radioContainer, toggleContainer) {
    if (!radioContainer) return;
    
    // Use MutationObserver to watch for changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' || mutation.type === 'childList') {
                // Check current radio state
                const checkedRadio = radioContainer.querySelector('input[type="radio"]:checked');
                if (checkedRadio) {
                    const isActive = checkedRadio.value === 'yes';
                    updateToggleVisualState(toggleContainer, isActive);
                }
            }
        });
    });
    
    observer.observe(radioContainer, {
        attributes: true,
        childList: true,
        subtree: true,
        attributeFilter: ['checked']
    });
    
    // Also listen for change events
    radioContainer.addEventListener('change', function() {
        const checkedRadio = radioContainer.querySelector('input[type="radio"]:checked');
        if (checkedRadio) {
            const isActive = checkedRadio.value === 'yes';
            updateToggleVisualState(toggleContainer, isActive);
        }
    });
}

// Floor slider display update
function updateFloorDisplay() {
    const floorSlider = document.querySelector('#num-floors-input');
    const floorDisplay = document.querySelector('#num-floors-display');
    
    if (floorSlider && floorDisplay) {
        const value = floorSlider.value || 4;
        const floors = parseInt(value);
        const text = floors === 1 ? '1 floor' : `${floors} floors`;
        floorDisplay.textContent = text;
    }
}

// Re-initialize toggles when new content is added (for dynamic content)
function reinitializeToggles() {
    initializeToggleSwitches();
}

// Expose functions globally for Dash integration
window.toggleFunctionality = {
    initialize: initializeToggleSwitches,
    reinitialize: reinitializeToggles,
    updateFloorDisplay: updateFloorDisplay
};

// Watch for dynamically added content
const bodyObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            // Check if any added nodes contain toggle containers
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    const toggles = node.querySelectorAll ? node.querySelectorAll('.toggle-container') : [];
                    if (toggles.length > 0 || node.classList?.contains('toggle-container')) {
                        setTimeout(initializeToggleSwitches, 100); // Small delay to ensure DOM is ready
                    }
                }
            });
        }
    });
});

bodyObserver.observe(document.body, {
    childList: true,
    subtree: true
});

console.log('Toggle functionality script loaded and initialized');