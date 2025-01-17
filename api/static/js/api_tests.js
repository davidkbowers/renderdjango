// Base API URL - change this according to your environment
const API_BASE_URL = 'http://localhost:8000/api';

// Utility function to handle API responses
const handleResponse = async (response) => {
    if (!response.ok) {
        const error = await response.json();
        throw new Error(JSON.stringify(error));
    }
    return response.json();
};

// Contact Form Tests
const testContactForm = async () => {
    console.group('Contact Form Tests');
    try {
        // Test valid submission
        const validData = {
            name: 'John Doe',
            email: 'john@example.com',
            message: 'This is a test message'
        };
        
        const response = await fetch(`${API_BASE_URL}/contact/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(validData)
        });
        
        const result = await handleResponse(response);
        console.log('✅ Valid contact form submission:', result);

        // Test invalid submission
        const invalidData = {
            name: '',
            email: 'invalid-email',
            message: ''
        };
        
        try {
            await fetch(`${API_BASE_URL}/contact/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(invalidData)
            }).then(handleResponse);
        } catch (error) {
            console.log('✅ Invalid contact form correctly rejected:', error.message);
        }
    } catch (error) {
        console.error('❌ Contact form test failed:', error);
    }
    console.groupEnd();
};

// Event Tests
const testEvents = async () => {
    console.group('Event Tests');
    try {
        // Test creating an event
        const newEvent = {
            title: 'Test Event',
            description: 'Test Description',
            eventdatetime: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
            address: '123 Test St',
            price: '99.99'
        };
        
        const createResponse = await fetch(`${API_BASE_URL}/events/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newEvent)
        }).then(handleResponse);
        
        console.log('✅ Event created:', createResponse);
        
        // Test listing events
        const listResponse = await fetch(`${API_BASE_URL}/events/`)
            .then(handleResponse);
        console.log('✅ Events listed:', listResponse);
        
        // Test getting single event
        const eventId = createResponse.id;
        const getResponse = await fetch(`${API_BASE_URL}/events/${eventId}/`)
            .then(handleResponse);
        console.log('✅ Single event retrieved:', getResponse);
        
        // Test updating event
        const updateData = {
            ...newEvent,
            title: 'Updated Test Event'
        };
        
        const updateResponse = await fetch(`${API_BASE_URL}/events/${eventId}/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updateData)
        }).then(handleResponse);
        
        console.log('✅ Event updated:', updateResponse);
        
        // Test deleting event
        const deleteResponse = await fetch(`${API_BASE_URL}/events/${eventId}/`, {
            method: 'DELETE'
        });
        
        console.log('✅ Event deleted:', deleteResponse.status === 204);
        
    } catch (error) {
        console.error('❌ Event tests failed:', error);
    }
    console.groupEnd();
};

// Registration Tests
const testRegistrations = async () => {
    console.group('Registration Tests');
    try {
        // First create an event for registration
        const event = {
            title: 'Registration Test Event',
            description: 'Test Description',
            eventdatetime: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
            address: '123 Test St',
            price: '99.99'
        };
        
        const eventResponse = await fetch(`${API_BASE_URL}/events/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(event)
        }).then(handleResponse);
        
        // Test creating a registration
        const registration = {
            date_registered: new Date().toISOString(),
            email: 'test@example.com',
            event: eventResponse.id
        };
        
        const createResponse = await fetch(`${API_BASE_URL}/registrations/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(registration)
        }).then(handleResponse);
        
        console.log('✅ Registration created:', createResponse);
        
        // Test listing registrations
        const listResponse = await fetch(`${API_BASE_URL}/registrations/`)
            .then(handleResponse);
        console.log('✅ Registrations listed:', listResponse);
        
        // Test filtering registrations by event
        const filteredResponse = await fetch(`${API_BASE_URL}/registrations/?event=${eventResponse.id}`)
            .then(handleResponse);
        console.log('✅ Filtered registrations:', filteredResponse);
        
    } catch (error) {
        console.error('❌ Registration tests failed:', error);
    }
    console.groupEnd();
};

// Subscriber Tests
const testSubscribers = async () => {
    console.group('Subscriber Tests');
    try {
        // Test creating a subscriber
        const subscriber = {
            name: 'Test Subscriber',
            email: 'subscriber@example.com'
        };
        
        const createResponse = await fetch(`${API_BASE_URL}/subscribers/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(subscriber)
        }).then(handleResponse);
        
        console.log('✅ Subscriber created:', createResponse);
        
        // Test listing subscribers
        const listResponse = await fetch(`${API_BASE_URL}/subscribers/`)
            .then(handleResponse);
        console.log('✅ Subscribers listed:', listResponse);
        
        // Test duplicate email validation
        try {
            await fetch(`${API_BASE_URL}/subscribers/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(subscriber)
            }).then(handleResponse);
        } catch (error) {
            console.log('✅ Duplicate email correctly rejected:', error.message);
        }
        
        // Test opt-out (soft delete)
        const deleteResponse = await fetch(`${API_BASE_URL}/subscribers/${createResponse.id}/`, {
            method: 'DELETE'
        });
        
        console.log('✅ Subscriber opted out:', deleteResponse.status === 204);
        
    } catch (error) {
        console.error('❌ Subscriber tests failed:', error);
    }
    console.groupEnd();
};

// Run all tests
const runAllTests = async () => {
    console.log('Starting API Tests...');
    await testContactForm();
    await testEvents();
    await testRegistrations();
    await testSubscribers();
    console.log('All tests completed!');
};

// HTML Elements for manual test running
const createTestButtons = () => {
    const container = document.createElement('div');
    container.style.padding = '20px';
    container.style.fontFamily = 'Arial, sans-serif';

    const title = document.createElement('h2');
    title.textContent = 'API Test Suite';
    container.appendChild(title);

    const buttons = [
        { text: 'Test Contact Form', fn: testContactForm },
        { text: 'Test Events', fn: testEvents },
        { text: 'Test Registrations', fn: testRegistrations },
        { text: 'Test Subscribers', fn: testSubscribers },
        { text: 'Run All Tests', fn: runAllTests }
    ];

    buttons.forEach(({ text, fn }) => {
        const button = document.createElement('button');
        button.textContent = text;
        button.onclick = fn;
        button.style.margin = '5px';
        button.style.padding = '10px';
        button.style.cursor = 'pointer';
        container.appendChild(button);
    });

    document.body.appendChild(container);
};

// Create test buttons when the page loads
window.onload = createTestButtons;
