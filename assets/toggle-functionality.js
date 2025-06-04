// assets/toggle-functionality.js
// Fixed Modern Toggle Switch Functionality for Dash Integration

document.addEventListener('DOMContentLoaded', function() {
    console.log('🎛️ Toggle functionality loaded');
    setTimeout(initializeToggleSwitches, 100); // Small delay to ensure DOM is ready
});

// Initialize toggle switch functionality
function initializeToggleSwitches() {
    console.log('🔄 Initializing toggle switches...');
    
    // Find all toggle containers
    const toggleContainers = document.querySelectorAll('.toggle-container');
    console.log(`Found ${toggleContainers.length} toggle containers`);
    
    toggleContainers.forEach((container, index) => {
        console.log(`Setting up toggle ${index + 1}`);
        setupToggleSwitch(container);
    });
}

// Setup individual toggle switch
function setupToggleSwitch(container) {
    const toggleSwitch = container.querySelector('.toggle-switch');
    const leftLabel = container.querySelector('.toggle-label-left');
    const rightLabel = container.querySelector('.toggle-label-right');
    
    if (!toggleSwitch) {
        console.warn('Toggle switch element not found');
        return;
    }
    
    // Find the associated hidden radio items - improved search
    const radioItems = findAssociatedRadioItems(container);
    
    if (!radioItems) {
        console.warn('No associated radio items found for toggle switch');
        return;
    }
    
    console.log('✅ Found radio items:', radioItems.id);
    
    // Set initial state based on radio button value
    const currentValue = getCurrentRadioValue(radioItems);
    updateToggleVisualState(container, currentValue === 'yes');
    
    // Add click event listener to the entire toggle container
    container.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        
        console.log('🖱️ Toggle clicked');
        
        // Toggle the state
        const isCurrentlyActive = toggleSwitch.classList.contains('active');
        const newValue = isCurrentlyActive ? 'no' : 'yes';
        
        console.log(`Toggling from ${isCurrentlyActive ? 'yes' : 'no'} to ${newValue}`);
        
        // Update the hidden radio button
        updateRadioValue(radioItems, newValue);
        
        // Update visual state
        updateToggleVisualState(container, newValue === 'yes');
        
        // Trigger change event for Dash callbacks - multiple methods
        triggerDashCallback(radioItems, newValue);
    });
    
    // Watch for external changes to radio buttons (from Dash)
    observeRadioChanges(radioItems, container);
    
    console.log('✅ Toggle switch setup complete');
}

// Improved function to find associated radio items
function findAssociatedRadioItems(container) {
    // Method 1: Look for radio items with manual-map-toggle ID in the same parent tree
    let parent = container.parentElement;
    let radioContainer = null;
    
    // Search up the DOM tree
    while (parent && parent !== document.body) {
        radioContainer = parent.querySelector('#manual-map-toggle');
        if (radioContainer) {
            console.log('Found radio container via parent search');
            break;
        }
        parent = parent.parentElement;
    }
    
    // Method 2: Direct document search if parent search fails
    if (!radioContainer) {
        radioContainer = document.querySelector('#manual-map-toggle');
        if (radioContainer) {
            console.log('Found radio container via document search');
        }
    }
    
    // Method 3: Look for any radio items in nearby containers
    if (!radioContainer) {
        const allRadioItems = document.querySelectorAll('input[type="radio"][value="yes"], input[type="radio"][value="no"]');
        for (let radio of allRadioItems) {
            const parentDiv = radio.closest('div[id*="manual"]');
            if (parentDiv) {
                radioContainer = parentDiv;
                console.log('Found radio container via radio input search');
                break;
            }
        }
    }
    
    return radioContainer;
}

// Get current radio value
function getCurrentRadioValue(radioContainer) {
    const checkedRadio = radioContainer.querySelector('input[type="radio"]:checked');
    return checkedRadio ? checkedRadio.value : 'no';
}

// Update toggle visual state
function updateToggleVisualState(container, isActive) {
    const toggleSwitch = container.querySelector('.toggle-switch');
    const leftLabel = container.querySelector('.toggle-label-left');
    const rightLabel = container.querySelector('.toggle-label-right');
    
    console.log(`Updating visual state: ${isActive ? 'active' : 'inactive'}`);
    
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

// Update radio button value - improved version
function updateRadioValue(radioContainer, value) {
    console.log(`Setting radio value to: ${value}`);
    
    // Find all radio inputs in the container
    const radioInputs = radioContainer.querySelectorAll('input[type="radio"]');
    
    radioInputs.forEach(input => {
        if (input.value === value) {
            input.checked = true;
            console.log(`✅ Set ${input.value} radio to checked`);
        } else {
            input.checked = false;
        }
    });
    
    // Also try to update the Dash component's value property directly
    if (radioContainer._dash_renderer && radioContainer._dash_renderer.value !== value) {
        radioContainer._dash_renderer.value = value;
        console.log(`✅ Updated Dash renderer value to: ${value}`);
    }
}

// Enhanced Dash callback triggering
function triggerDashCallback(radioContainer, newValue) {
    console.log(`🎯 Triggering Dash callback with value: ${newValue}`);
    
    // Method 1: Trigger on the checked radio input
    const checkedRadio = radioContainer.querySelector(`input[type="radio"][value="${newValue}"]`);
    if (checkedRadio) {
        // Multiple event types to ensure Dash picks it up
        ['change', 'input', 'click'].forEach(eventType => {
            const event = new Event(eventType, { 
                bubbles: true, 
                cancelable: true,
                composed: true 
            });
            checkedRadio.dispatchEvent(event);
        });
        console.log('✅ Dispatched events on radio input');
    }
    
    // Method 2: Trigger on the radio container
    ['change', 'input'].forEach(eventType => {
        const containerEvent = new Event(eventType, { 
            bubbles: true, 
            cancelable: true,
            composed: true 
        });
        radioContainer.dispatchEvent(containerEvent);
    });
    console.log('✅ Dispatched events on radio container');
    
    // Method 3: Try to trigger Dash directly if available
    if (window.dash_clientside && window.dash_clientside.callback_context) {
        try {
            // Update Dash's internal state
            window.dash_clientside.callback_context.triggered = [{
                prop_id: 'manual-map-toggle.value',
                value: newValue
            }];
            console.log('✅ Updated Dash callback context');
        } catch (e) {
            console.log('⚠️ Could not update Dash context:', e);
        }
    }
    
    // Method 4: Custom event for Dash
    const dashEvent = new CustomEvent('dash-update', {
        detail: {
            component_id: 'manual-map-toggle',
            value: newValue
        },
        bubbles: true
    });
    document.dispatchEvent(dashEvent);
    console.log('✅ Dispatched custom Dash event');
}

// Observe radio button changes from external sources (Dash callbacks)
function observeRadioChanges(radioContainer, toggleContainer) {
    if (!radioContainer) return;
    
    // Use MutationObserver to watch for changes
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' || mutation.type === 'childList') {
                // Check current radio state
                const currentValue = getCurrentRadioValue(radioContainer);
                const isActive = currentValue === 'yes';
                updateToggleVisualState(toggleContainer, isActive);
                console.log(`📡 External change detected: ${currentValue}`);
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
    radioContainer.addEventListener('change', function(e) {
        const currentValue = getCurrentRadioValue(radioContainer);
        const isActive = currentValue === 'yes';
        updateToggleVisualState(toggleContainer, isActive);
        console.log(`📻 Radio change event: ${currentValue}`);
    });
    
    console.log('👀 Set up radio change observers');
}

// Re-initialize toggles when new content is added (for dynamic content)
function reinitializeToggles() {
    console.log('🔄 Reinitializing toggles...');
    initializeToggleSwitches();
}

// Watch for dynamically added content - improved version
const bodyObserver = new MutationObserver(function(mutations) {
    let shouldReinitialize = false;
    
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) { // Element node
                    // Check if any added nodes contain toggle containers
                    const toggles = node.querySelectorAll ? node.querySelectorAll('.toggle-container') : [];
                    const hasToggleClass = node.classList && node.classList.contains('toggle-container');
                    const hasRadioItems = node.querySelectorAll ? node.querySelectorAll('#manual-map-toggle').length > 0 : false;
                    
                    if (toggles.length > 0 || hasToggleClass || hasRadioItems) {
                        shouldReinitialize = true;
                    }
                }
            });
        }
    });
    
    if (shouldReinitialize) {
        console.log('🆕 New toggle content detected, reinitializing...');
        setTimeout(initializeToggleSwitches, 100); // Small delay to ensure DOM is ready
    }
});

bodyObserver.observe(document.body, {
    childList: true,
    subtree: true
});

// Expose functions globally for manual testing and Dash integration
window.toggleFunctionality = {
    initialize: initializeToggleSwitches,
    reinitialize: reinitializeToggles,
    test: function() {
        console.log('🧪 Testing toggle functionality...');
        const radioContainer = document.querySelector('#manual-map-toggle');
        const toggleContainer = document.querySelector('.toggle-container');
        
        console.log('Radio container:', radioContainer);
        console.log('Toggle container:', toggleContainer);
        console.log('Current radio value:', radioContainer ? getCurrentRadioValue(radioContainer) : 'not found');
        
        if (radioContainer && toggleContainer) {
            console.log('✅ All components found - toggle should work');
        } else {
            console.log('❌ Missing components - toggle may not work');
        }
    }
};

// Debug function to check toggle state
function debugToggleState() {
    const radioContainer = document.querySelector('#manual-map-toggle');
    const toggleContainer = document.querySelector('.toggle-container');
    
    console.log('=== TOGGLE DEBUG INFO ===');
    console.log('Radio container found:', !!radioContainer);
    console.log('Toggle container found:', !!toggleContainer);
    
    if (radioContainer) {
        const currentValue = getCurrentRadioValue(radioContainer);
        console.log('Current radio value:', currentValue);
        
        const allRadios = radioContainer.querySelectorAll('input[type="radio"]');
        console.log('Radio options:', Array.from(allRadios).map(r => ({
            value: r.value,
            checked: r.checked
        })));
    }
    
    if (toggleContainer) {
        const toggleSwitch = toggleContainer.querySelector('.toggle-switch');
        console.log('Toggle active:', toggleSwitch ? toggleSwitch.classList.contains('active') : 'switch not found');
    }
    console.log('========================');
}

// Add color management for radio buttons
function applyRadioColors() {
    const radioContainer = document.querySelector('#manual-map-toggle');
    if (!radioContainer) return;
    
    const labels = radioContainer.querySelectorAll('label');
    const inputs = radioContainer.querySelectorAll('input[type="radio"]');
    
    inputs.forEach((input, index) => {
        const label = labels[index];
        if (!label) return;
        
        if (input.checked) {
            if (input.value === 'no') {
                label.style.backgroundColor = '#E02020'; // Red
                label.style.borderColor = '#E02020';
                label.style.color = 'white';
            } else if (input.value === 'yes') {
                label.style.backgroundColor = '#2196F3'; // Blue  
                label.style.borderColor = '#2196F3';
                label.style.color = 'white';
            }
        } else {
            label.style.backgroundColor = '#2D3748'; // Gray
            label.style.borderColor = '#4A5568';
            label.style.color = '#A0AEC0';
        }
    });
}

// Apply colors on page load and radio change
document.addEventListener('DOMContentLoaded', applyRadioColors);
document.addEventListener('change', applyRadioColors);

// Radio Toggle Color Fix - Works 100%
function fixRadioColors() {
    const container = document.querySelector('#manual-map-toggle');
    if (!container) return;
    
    const labels = container.querySelectorAll('label');
    const inputs = container.querySelectorAll('input[type="radio"]');
    
    // Apply colors based on which radio is checked
    inputs.forEach((input, index) => {
        const label = labels[index];
        if (!label) return;
        
        if (input.checked) {
            if (input.value === 'no') {
                // RED for No
                label.style.backgroundColor = '#E02020';
                label.style.borderColor = '#E02020';
                label.style.color = 'white';
                label.style.fontWeight = '600';
                label.style.boxShadow = '0 2px 8px rgba(224, 32, 32, 0.3)';
            } else if (input.value === 'yes') {
                // BLUE for Yes
                label.style.backgroundColor = '#2196F3';
                label.style.borderColor = '#2196F3';
                label.style.color = 'white';
                label.style.fontWeight = '600';
                label.style.boxShadow = '0 2px 8px rgba(33, 150, 243, 0.3)';
            }
        } else {
            // GRAY for unselected
            label.style.backgroundColor = '#2D3748';
            label.style.borderColor = '#4A5568';
            label.style.color = '#A0AEC0';
            label.style.fontWeight = '500';
            label.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
        }
    });
}

// Apply on load and changes
document.addEventListener('DOMContentLoaded', () => setTimeout(fixRadioColors, 100));
document.addEventListener('click', () => setTimeout(fixRadioColors, 50));
document.addEventListener('change', () => setTimeout(fixRadioColors, 50));

// Watch for new content
new MutationObserver(() => setTimeout(fixRadioColors, 100))
    .observe(document.body, { childList: true, subtree: true });


    
// Test function
window.testRadioColors = () => {
    console.log('Testing radio colors...');
    fixRadioColors();
    console.log('Colors applied!');
};

// Expose debug function
window.debugToggle = debugToggleState;
// ═══════════════════════════════════════════════════════════════════════════════
// RADIO TOGGLE FIX - ADD THIS TO THE END OF YOUR EXISTING toggle-functionality.js
// ═══════════════════════════════════════════════════════════════════════════════

// Fix for radio toggle color and functionality issues
document.addEventListener('DOMContentLoaded', function() {
    console.log('🔧 Radio toggle fix loading...');
    setTimeout(fixRadioToggleIssues, 300);
});

function fixRadioToggleIssues() {
    const radioContainer = document.querySelector('#manual-map-toggle');
    
    if (!radioContainer) {
        console.warn('❌ Radio container not found, retrying...');
        setTimeout(fixRadioToggleIssues, 500);
        return;
    }
    
    console.log('✅ Fixing radio toggle issues...');
    
    // Apply initial styling
    applyRadioToggleFix();
    
    // Set up event listeners for real-time updates
    setupRadioToggleListeners(radioContainer);
    
    // Watch for changes
    observeRadioToggleChanges(radioContainer);
}

function applyRadioToggleFix() {
    const radioContainer = document.querySelector('#manual-map-toggle');
    if (!radioContainer) return;
    
    const radioInputs = radioContainer.querySelectorAll('input[type="radio"]');
    const labels = radioContainer.querySelectorAll('label');
    
    console.log(`🎨 Styling ${radioInputs.length} radio inputs`);
    
    radioInputs.forEach((input, index) => {
        const label = labels[index];
        if (!label) return;
        
        // Hide radio input completely
        input.style.display = 'none';
        input.style.opacity = '0';
        input.style.position = 'absolute';
        input.style.left = '-9999px';
        
        // Style the label as button
        applyLabelStyling(label);
        
        // Apply checked state
        if (input.checked) {
            applyCheckedStyling(label, input.value);
            console.log(`✅ Applied checked styling for: ${input.value}`);
        }
    });
}

function applyLabelStyling(label) {
    Object.assign(label.style, {
        display: 'inline-block',
        backgroundColor: '#2D3748',
        color: '#A0AEC0',
        border: '2px solid #4A5568',
        borderRadius: '20px',
        padding: '10px 24px',
        margin: '0 8px',
        cursor: 'pointer',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        fontWeight: '500',
        minWidth: '80px',
        textAlign: 'center',
        userSelect: 'none',
        fontSize: '0.9rem',
        boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)'
    });
}

function applyCheckedStyling(label, value) {
    label.style.color = 'white';
    label.style.fontWeight = '600';
    label.style.transform = 'translateY(-1px)';
    
    if (value === 'yes') {
        label.style.backgroundColor = '#2196F3';
        label.style.borderColor = '#2196F3';
        label.style.boxShadow = '0 2px 8px rgba(33, 150, 243, 0.4)';
    } else if (value === 'no') {
        label.style.backgroundColor = '#E02020';
        label.style.borderColor = '#E02020';
        label.style.boxShadow = '0 2px 8px rgba(224, 32, 32, 0.4)';
    }
}

function setupRadioToggleListeners(container) {
    // Listen for changes on the container
    container.addEventListener('change', function(e) {
        if (e.target.type === 'radio') {
            console.log('📻 Radio changed to:', e.target.value);
            setTimeout(applyRadioToggleFix, 50);
        }
    });
    
    // Add click handlers to labels
    const labels = container.querySelectorAll('label');
    labels.forEach((label, index) => {
        label.addEventListener('click', function(e) {
            const radioInputs = container.querySelectorAll('input[type="radio"]');
            const targetInput = radioInputs[index];
            
            if (targetInput && !targetInput.checked) {
                targetInput.checked = true;
                
                // Trigger Dash callback
                ['change', 'input', 'click'].forEach(eventType => {
                    const event = new Event(eventType, { bubbles: true, cancelable: true });
                    targetInput.dispatchEvent(event);
                });
                
                // Update styling
                setTimeout(applyRadioToggleFix, 50);
                console.log(`🖱️ Manually selected: ${targetInput.value}`);
            }
        });
    });
}

function observeRadioToggleChanges(container) {
    const observer = new MutationObserver(function(mutations) {
        let shouldUpdate = false;
        
        mutations.forEach(function(mutation) {
            if (mutation.type === 'attributes' && 
                (mutation.attributeName === 'checked' || mutation.attributeName === 'value')) {
                shouldUpdate = true;
            }
        });
        
        if (shouldUpdate) {
            console.log('🔄 Radio state mutated, updating...');
            setTimeout(applyRadioToggleFix, 50);
        }
    });
    
    observer.observe(container, {
        attributes: true,
        childList: true,
        subtree: true,
        attributeFilter: ['checked', 'value']
    });
}

// Debug functions
window.debugRadioToggleFixed = function() {
    console.log('=== RADIO TOGGLE DEBUG (FIXED) ===');
    
    const container = document.querySelector('#manual-map-toggle');
    if (!container) {
        console.log('❌ Container not found');
        return;
    }
    
    const radios = container.querySelectorAll('input[type="radio"]');
    const labels = container.querySelectorAll('label');
    
    console.log(`📊 Found ${radios.length} radios, ${labels.length} labels`);
    
    radios.forEach((radio, i) => {
        console.log(`Radio ${i}: value=${radio.value}, checked=${radio.checked}`);
    });
    
    labels.forEach((label, i) => {
        console.log(`Label ${i}: bg=${label.style.backgroundColor}, color=${label.style.color}`);
    });
};

window.forceRadioToggleUpdate = function() {
    console.log('🔄 Forcing radio toggle update...');
    applyRadioToggleFix();
};

// Auto-fix on page mutations
const pageObserver = new MutationObserver(function(mutations) {
    mutations.forEach(function(mutation) {
        if (mutation.addedNodes.length > 0) {
            mutation.addedNodes.forEach(function(node) {
                if (node.nodeType === 1) {
                    const hasRadioToggle = node.querySelector && node.querySelector('#manual-map-toggle');
                    const isRadioToggle = node.id === 'manual-map-toggle';
                    
                    if (hasRadioToggle || isRadioToggle) {
                        console.log('🆕 New radio toggle detected, applying fix...');
                        setTimeout(fixRadioToggleIssues, 100);
                    }
                }
            });
        }
    });
});

pageObserver.observe(document.body, { childList: true, subtree: true });

console.log('🎛️ Radio toggle fix script loaded');
console.log('💡 Use window.debugRadioToggleFixed() to debug');
console.log('🔧 Use window.forceRadioToggleUpdate() to force update');