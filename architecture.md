# NYC Sticker Wiki - Test Version Architecture

## Overview
A simplified version of the sticker wiki focusing on core functionality:
- Upload sticker photos
- Basic image matching
- Wiki-style content editing
- Simple map of sightings

## Components

### Frontend
- Simple HTML/CSS/JavaScript
- Single page design with:
  - Upload form
  - Sticker gallery
  - Basic content editor
  - Map view using Leaflet.js

### Backend (Flask)
- Simple REST API endpoints:
  - `/upload` - Handle image uploads
  - `/stickers` - CRUD operations for stickers
  - `/sightings` - Record sticker locations
  - `/content` - Wiki content management

### Database (SQLite)
Simple schema:
```sql
CREATE TABLE stickers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    description TEXT,
    created_at TIMESTAMP
);

CREATE TABLE sightings (
    id INTEGER PRIMARY KEY,
    sticker_id INTEGER,
    latitude REAL,
    longitude REAL,
    image_path TEXT,
    spotted_at TIMESTAMP,
    FOREIGN KEY (sticker_id) REFERENCES stickers(id)
);

CREATE TABLE wiki_content (
    id INTEGER PRIMARY KEY,
    sticker_id INTEGER,
    content TEXT,
    updated_at TIMESTAMP,
    FOREIGN KEY (sticker_id) REFERENCES stickers(id)
);
```

### Storage
- Local file system storage in `/uploads` directory
- Simple directory structure:
  - `/uploads/stickers/` - Original sticker images
  - `/uploads/sightings/` - Sighting photos

### Image Matching
- Basic image comparison using OpenCV
- Simple feature matching algorithm
- Store feature data in memory for quick matching

## Implementation Plan

1. Setup Basic Structure
   - Create Flask project
   - Setup SQLite database
   - Create upload directory

2. Backend Implementation
   - Image upload handling
   - Basic database operations
   - Simple image comparison logic

3. Frontend Implementation
   - Upload form
   - Gallery view
   - Basic map integration
   - Wiki content editor

4. Integration
   - Connect frontend to backend
   - Test core workflows

## Core Workflows

### Upload Flow
1. User uploads photo
2. Backend saves image to local storage
3. Basic image comparison runs
4. Create new sticker or add sighting
5. Show result to user

### Content Editing
1. Select sticker from gallery
2. Edit description in text area
3. Save changes to database

### Map View
1. Load sightings from database
2. Display markers on map
3. Click marker to view sticker info

## File Structure
```
sticker-wiki/
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── main.js
│   └── uploads/
│       ├── stickers/
│       └── sightings/
├── templates/
│   └── index.html
├── app.py
├── database.py
└── image_matcher.py
```

This simplified architecture focuses on getting core functionality working without the complexity of authentication, optimization, or scalability concerns. It can serve as a proof of concept and testing ground for the core features before expanding to a more robust solution.