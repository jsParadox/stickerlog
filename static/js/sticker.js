// Initialize map
const map = L.map('map').setView([40.7128, -74.0060], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Store markers
const markers = new Map();

// Get sticker ID from the page
const stickerId = document.getElementById('sticker-title').dataset.stickerId;

// Wiki editing functionality
const editWikiBtn = document.getElementById('edit-wiki');
const wikiDisplay = document.getElementById('wiki-display');
const wikiEditor = document.getElementById('wiki-editor');
const wikiText = document.getElementById('wiki-text');
const saveWikiBtn = document.getElementById('save-wiki');
const cancelWikiBtn = document.getElementById('cancel-wiki');

editWikiBtn.addEventListener('click', () => {
    wikiEditor.classList.remove('hidden');
    wikiDisplay.classList.add('hidden');
    wikiText.value = wikiDisplay.textContent.trim();
});

cancelWikiBtn.addEventListener('click', () => {
    wikiEditor.classList.add('hidden');
    wikiDisplay.classList.remove('hidden');
    wikiText.value = wikiDisplay.textContent.trim();
});

saveWikiBtn.addEventListener('click', async () => {
    const content = wikiText.value;
    
    try {
        const response = await fetch(`/api/stickers/${stickerId}/wiki`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ content })
        });
        
        if (response.ok) {
            wikiDisplay.innerHTML = marked.parse(content); // Using marked for Markdown parsing
            wikiEditor.classList.add('hidden');
            wikiDisplay.classList.remove('hidden');
            showStatus('Wiki content updated!', 'success');
        } else {
            const data = await response.json();
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error saving wiki content:', error);
        showStatus('Error saving wiki content', 'error');
    }
});

// Load sightings
async function loadSightings() {
    try {
        const response = await fetch(`/api/stickers/${stickerId}`);
        const data = await response.json();
        
        // Clear existing markers
        markers.forEach(marker => map.removeLayer(marker));
        markers.clear();
        
        // Update sightings list and map
        const sightingsList = document.getElementById('sightings-list');
        sightingsList.innerHTML = '';
        
        data.sightings.forEach(sighting => {
            // Add marker to map
            const marker = L.marker([sighting.latitude, sighting.longitude])
                .bindPopup(`Spotted: ${new Date(sighting.spotted_at).toLocaleDateString()}`);
            markers.set(sighting.id, marker);
            marker.addTo(map);
            
            // Add to sightings list
            const sightingCard = document.createElement('div');
            sightingCard.className = 'sighting-card';
            sightingCard.innerHTML = `
                <img src="/uploads/sightings/${sighting.id}_sighting.jpg" alt="Sighting">
                <div class="sighting-info">
                    <p>Spotted: ${new Date(sighting.spotted_at).toLocaleDateString()}</p>
                    <p>Location: ${sighting.latitude.toFixed(6)}, ${sighting.longitude.toFixed(6)}</p>
                </div>
            `;
            sightingsList.appendChild(sightingCard);
        });
        
        // Fit map to show all markers
        if (data.sightings.length > 0) {
            const bounds = L.latLngBounds(data.sightings.map(s => [s.latitude, s.longitude]));
            map.fitBounds(bounds.pad(0.1));
        }
        
        // Update quick facts
        document.getElementById('first-spotted').textContent = 
            new Date(data.sightings[data.sightings.length - 1].spotted_at).toLocaleDateString();
        document.getElementById('sighting-count').textContent = data.sightings.length;
        document.getElementById('last-updated').textContent = 
            new Date(data.wiki_content?.updated_at || data.sticker.created_at).toLocaleDateString();
        
    } catch (error) {
        console.error('Error loading sightings:', error);
        showStatus('Error loading sightings', 'error');
    }
}

// Helper function to show status messages
function showStatus(message, type) {
    const statusDiv = document.createElement('div');
    statusDiv.textContent = message;
    statusDiv.className = `status-message ${type}`;
    document.querySelector('.wiki-header').appendChild(statusDiv);
    
    setTimeout(() => {
        statusDiv.remove();
    }, 5000);
}

// Load sightings when page loads
document.addEventListener('DOMContentLoaded', () => {
    loadSightings();
    
    // Add Markdown library for wiki content
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    document.head.appendChild(script);
});