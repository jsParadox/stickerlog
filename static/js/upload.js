// Initialize map centered on NYC
const map = L.map('map').setView([40.7128, -74.0060], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Current location and marker
let currentLocation = null;
let locationMarker = null;

// Get user's location
if ("geolocation" in navigator) {
    const locationStatus = document.querySelector('.location-status');
    
    navigator.geolocation.getCurrentPosition(position => {
        currentLocation = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
        };
        
        // Update map
        map.setView([currentLocation.latitude, currentLocation.longitude], 15);
        
        // Add/update marker
        if (locationMarker) {
            locationMarker.setLatLng([currentLocation.latitude, currentLocation.longitude]);
        } else {
            locationMarker = L.marker([currentLocation.latitude, currentLocation.longitude]).addTo(map);
        }
        
        locationStatus.textContent = 'Location detected!';
        locationStatus.style.color = '#2ecc71';
    }, error => {
        locationStatus.textContent = 'Error detecting location. Please try again.';
        locationStatus.style.color = '#e74c3c';
        console.error('Location error:', error);
    });
}

// Handle image preview
const imageInput = document.getElementById('sticker-image');
const previewDiv = document.querySelector('.image-preview');

imageInput.addEventListener('change', function() {
    const file = this.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            previewDiv.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
        };
        reader.readAsDataURL(file);
    } else {
        previewDiv.innerHTML = '';
    }
});

// Handle form submission
const uploadForm = document.getElementById('upload-form');
const uploadStatus = document.getElementById('upload-status');

function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = type;
    setTimeout(() => {
        uploadStatus.textContent = '';
        uploadStatus.className = '';
    }, 5000);
}

uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!currentLocation) {
        showStatus('Please allow location access to upload stickers', 'error');
        return;
    }

    const formData = new FormData();
    const fileInput = document.getElementById('sticker-image');
    const nameInput = document.getElementById('sticker-name');
    const descriptionInput = document.getElementById('sticker-description');

    if (!fileInput.files[0]) {
        showStatus('Please select an image', 'error');
        return;
    }

    formData.append('file', fileInput.files[0]);
    formData.append('latitude', currentLocation.latitude);
    formData.append('longitude', currentLocation.longitude);
    formData.append('name', nameInput.value || 'Unknown Sticker');
    formData.append('description', descriptionInput.value || '');

    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            if (data.match_found) {
                showStatus('Matched existing sticker! Adding new sighting.', 'success');
                setTimeout(() => {
                    window.location.href = `/sticker/${data.sticker.id}`;
                }, 1500);
            } else {
                showStatus('New sticker added!', 'success');
                setTimeout(() => {
                    window.location.href = `/sticker/${data.sticker_id}`;
                }, 1500);
            }
            
            // Reset form
            uploadForm.reset();
            previewDiv.innerHTML = '';
        } else {
            showStatus(`Error: ${data.error}`, 'error');
        }
    } catch (error) {
        showStatus('Error uploading sticker', 'error');
        console.error('Upload error:', error);
    }
});