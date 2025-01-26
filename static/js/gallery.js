// Load and display sticker gallery
async function loadGallery() {
    try {
        const response = await fetch('/api/stickers');
        const stickers = await response.json();
        
        const gallery = document.getElementById('sticker-gallery');
        gallery.innerHTML = '';
        
        stickers.forEach(sticker => {
            const card = document.createElement('div');
            card.className = 'sticker-card';
            card.innerHTML = `
                <img src="/uploads/stickers/${sticker.id}_sticker.jpg" alt="${sticker.name}">
                <div class="sticker-card-content">
                    <h3>${sticker.name}</h3>
                    <p>${sticker.description ? sticker.description.substring(0, 100) + '...' : 'No description available.'}</p>
                </div>
            `;
            card.addEventListener('click', () => {
                window.location.href = `/sticker/${sticker.id}`;
            });
            gallery.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading gallery:', error);
        const gallery = document.getElementById('sticker-gallery');
        gallery.innerHTML = '<p class="error">Error loading stickers. Please try again later.</p>';
    }
}

// Load gallery when page loads
document.addEventListener('DOMContentLoaded', loadGallery);