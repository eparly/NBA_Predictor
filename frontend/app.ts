// app.js

const API_ENDPOINT = 'https://your-api-id.execute-api.region.amazonaws.com/dev/data';

async function fetchData() {
    try {
        const response = await fetch(API_ENDPOINT);
        const data = await response.json();
        document.getElementById('data-display').textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error('Error fetching data:', error);
        document.getElementById('data-display').textContent = 'Error fetching data';
    }
}
