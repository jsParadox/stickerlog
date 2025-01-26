from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for
import os
from werkzeug.utils import secure_filename
from database import init_db, add_sticker, add_sighting, update_wiki_content, get_sticker, get_all_stickers, get_sticker_sightings, get_wiki_content
from image_matcher import ImageMatcher
from pathlib import Path
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Initialize database and image matcher
init_db()
image_matcher = ImageMatcher()

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'jpg', 'jpeg', 'png'}

@app.route('/')
def index():
    """Render the gallery page."""
    return render_template('index.html')

@app.route('/upload')
def upload():
    """Render the upload page."""
    return render_template('upload.html')

@app.route('/sticker/<int:sticker_id>')
def sticker_page(sticker_id):
    """Render the sticker detail page."""
    sticker = get_sticker(sticker_id)
    if not sticker:
        return redirect(url_for('index'))
    
    wiki_content = get_wiki_content(sticker_id)
    sightings = get_sticker_sightings(sticker_id)
    
    # Calculate statistics
    sighting_count = len(sightings)
    first_spotted = min(sightings, key=lambda x: x['spotted_at'])['spotted_at'] if sightings else sticker['created_at']
    last_updated = wiki_content['updated_at'] if wiki_content else sticker['created_at']
    
    return render_template('sticker.html',
                         sticker=sticker,
                         wiki_content=wiki_content['content'] if wiki_content else '',
                         sighting_count=sighting_count,
                         first_spotted=first_spotted,
                         last_updated=last_updated)

@app.route('/api/upload', methods=['POST'])
def upload_sticker():
    """Handle sticker upload and matching."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_path = Path(app.config['UPLOAD_FOLDER']) / 'temp' / filename
        temp_path.parent.mkdir(exist_ok=True)
        file.save(str(temp_path))

        # Get location data
        latitude = request.form.get('latitude', type=float)
        longitude = request.form.get('longitude', type=float)

        # Try to find matches
        matches = image_matcher.find_matches(str(temp_path))

        if matches and matches[0][1] > 0.3:  # If good match found
            # Add new sighting
            sticker_id = matches[0][0]
            sighting_id = add_sighting(sticker_id, latitude, longitude, str(temp_path))
            
            # Save sighting image
            image_path = image_matcher.save_sighting_image(str(temp_path), sighting_id)
            
            # Get sticker details
            sticker = get_sticker(sticker_id)
            
            return jsonify({
                'match_found': True,
                'sticker': sticker,
                'sighting_id': sighting_id
            })
        else:
            # Create new sticker
            name = request.form.get('name', 'Unknown Sticker')
            description = request.form.get('description', '')
            
            sticker_id = add_sticker(name, description)
            
            # Save sticker image
            image_matcher.save_sticker_image(str(temp_path), sticker_id)
            
            # Add first sighting
            sighting_id = add_sighting(sticker_id, latitude, longitude, str(temp_path))
            image_matcher.save_sighting_image(str(temp_path), sighting_id)
            
            return jsonify({
                'match_found': False,
                'sticker_id': sticker_id,
                'sighting_id': sighting_id
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    finally:
        # Clean up temporary file
        if temp_path.exists():
            temp_path.unlink()

@app.route('/api/stickers', methods=['GET'])
def get_stickers():
    """Get all stickers."""
    stickers = get_all_stickers()
    return jsonify(stickers)

@app.route('/api/stickers/<int:sticker_id>', methods=['GET'])
def get_sticker_details(sticker_id):
    """Get details for a specific sticker."""
    sticker = get_sticker(sticker_id)
    if not sticker:
        return jsonify({'error': 'Sticker not found'}), 404
    
    sightings = get_sticker_sightings(sticker_id)
    wiki_content = get_wiki_content(sticker_id)
    
    return jsonify({
        'sticker': sticker,
        'sightings': sightings,
        'wiki_content': wiki_content
    })

@app.route('/api/stickers/<int:sticker_id>/wiki', methods=['POST'])
def update_sticker_wiki(sticker_id):
    """Update wiki content for a sticker."""
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    content = request.json.get('content')
    if not content:
        return jsonify({'error': 'No content provided'}), 400
    
    update_wiki_content(sticker_id, content)
    return jsonify({'success': True})

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded files."""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    # Ensure upload directories exist
    Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)
    (Path(app.config['UPLOAD_FOLDER']) / 'stickers').mkdir(exist_ok=True)
    (Path(app.config['UPLOAD_FOLDER']) / 'sightings').mkdir(exist_ok=True)
    (Path(app.config['UPLOAD_FOLDER']) / 'temp').mkdir(exist_ok=True)
    
    app.run(debug=True)