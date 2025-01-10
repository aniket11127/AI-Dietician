// Error handling
function showError(message, containerId = 'error-container') {
    const container = document.getElementById(containerId);
    if (container) {
        container.innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
    }
}

// Chat functionality
function addMessage(message, isUser = false) {
    const chatContainer = document.getElementById('chat-container');
    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = message;
    chatContainer.appendChild(messageDiv);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    
    if (message) {
        addMessage(message, true);
        input.value = '';

        try {
            const response = await fetch('http://localhost:5000/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });

            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            const data = await response.json();
            if (data.error) {
                showError(data.error);
            } else {
                addMessage(data.response);
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Sorry, I encountered an error. Please try again.');
        }
    }
}

// Image handling
function handleImageError(img) {
    img.onerror = null; // Prevent infinite loop
    img.src = createPlaceholder(img.width, img.height, img.alt);
    img.classList.add('placeholder-img');
}

function createPlaceholder(width, height, text) {
    const canvas = document.createElement('canvas');
    canvas.width = width || 300;
    canvas.height = height || 200;
    const ctx = canvas.getContext('2d');
    
    // Fill background
    ctx.fillStyle = '#f8f9fa';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Add text
    ctx.fillStyle = '#6c757d';
    ctx.font = '14px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(text || 'Image not available', canvas.width/2, canvas.height/2);
    
    return canvas.toDataURL();
}

// Function to optimize image display in diet plan
function optimizeImage(url) {
    return url; // For local files, just return the URL as is
}

// Diet plan functionality
document.getElementById('user-profile-form').addEventListener('submit', async function(event) {
    event.preventDefault();
    
    // Show loading state
    document.getElementById('loading').style.display = 'block';
    document.getElementById('diet-plan-container').innerHTML = '';
    document.getElementById('error-container').innerHTML = '';
    
    try {
        const formData = {
            age: parseInt(document.getElementById('age').value),
            weight: parseFloat(document.getElementById('weight').value),
            height: parseFloat(document.getElementById('height').value),
            gender: document.getElementById('gender').value,
            activity_level: document.getElementById('activity_level').value,
            goal: document.getElementById('goal').value,
            dietary_preferences: Array.from(document.getElementById('dietary_preferences').selectedOptions).map(option => option.value),
            allergies: document.getElementById('allergies').value.split(',').map(allergy => allergy.trim()).filter(Boolean)
        };

        console.log('Sending form data:', formData); // Debug log

        const response = await fetch('http://localhost:5000/diet-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        console.log('Response status:', response.status); // Debug log
        const data = await response.json();
        console.log('Response data:', data); // Debug log
        
        // Hide loading state
        document.getElementById('loading').style.display = 'none';
        
        if (response.ok) {
            if (data.error) {
                showError(data.error);
            } else {
                displayDietPlan(data);
            }
        } else {
            showError(data.error || 'Failed to generate diet plan');
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('loading').style.display = 'none';
        showError('Failed to generate diet plan. Please try again.');
    }
});

function displayDietPlan(plan) {
    const container = document.getElementById('diet-plan-container');
    
    if (!plan || !plan.meals) {
        showError('Invalid diet plan data received');
        return;
    }
    
    console.log('Displaying plan:', plan); // Debug log
    
    container.innerHTML = `
        <div class="card mt-4">
            <div class="card-header bg-primary text-white">
                <h3 class="mb-0">Your Personalized Diet Plan</h3>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <h4>Daily Targets</h4>
                        <ul class="list-group mb-3">
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Calories
                                <span class="badge bg-primary rounded-pill">${Math.round(plan.daily_calories)} kcal</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Protein
                                <span class="badge bg-success rounded-pill">${Math.round(plan.macros.protein)}g</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Carbs
                                <span class="badge bg-info rounded-pill">${Math.round(plan.macros.carbs)}g</span>
                            </li>
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                Fat
                                <span class="badge bg-warning rounded-pill">${Math.round(plan.macros.fat)}g</span>
                            </li>
                        </ul>
                        <img src="images/macros-chart.png" alt="Macros Distribution" 
                             class="img-fluid rounded mb-3" onerror="handleImageError(this)" loading="lazy">
                    </div>
                    <div class="col-md-8">
                        <h4>Meal Plan</h4>
                        <div class="row">
                            ${['breakfast', 'lunch', 'dinner'].map(mealType => `
                                <div class="col-md-4">
                                    <div class="card mb-3">
                                        <img src="images/${mealType}.jpg" 
                                             class="card-img-top meal-image" alt="${mealType.charAt(0).toUpperCase() + mealType.slice(1)}"
                                             onerror="handleImageError(this)" loading="lazy">
                                        <div class="card-body">
                                            <h5>${mealType.charAt(0).toUpperCase() + mealType.slice(1)} Options</h5>
                                            <ul class="list-group list-group-flush">
                                                ${plan.meals[mealType] ? plan.meals[mealType].map(meal => `
                                                    <li class="list-group-item">${meal}</li>
                                                `).join('') : '<li class="list-group-item">No meals available</li>'}
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}
