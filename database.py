import sqlite3
from datetime import datetime

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('stickers.db')
    c = conn.cursor()

    # Create stickers table
    c.execute('''
        CREATE TABLE IF NOT EXISTS stickers (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            created_at TIMESTAMP
        )
    ''')

    # Create sightings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS sightings (
            id INTEGER PRIMARY KEY,
            sticker_id INTEGER,
            latitude REAL,
            longitude REAL,
            image_path TEXT,
            spotted_at TIMESTAMP,
            FOREIGN KEY (sticker_id) REFERENCES stickers(id)
        )
    ''')

    # Create wiki_content table
    c.execute('''
        CREATE TABLE IF NOT EXISTS wiki_content (
            id INTEGER PRIMARY KEY,
            sticker_id INTEGER,
            content TEXT,
            updated_at TIMESTAMP,
            FOREIGN KEY (sticker_id) REFERENCES stickers(id)
        )
    ''')

    conn.commit()
    conn.close()

def get_db():
    """Get a database connection."""
    conn = sqlite3.connect('stickers.db')
    conn.row_factory = sqlite3.Row
    return conn

def add_sticker(name, description):
    """Add a new sticker to the database."""
    conn = get_db()
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT INTO stickers (name, description, created_at)
        VALUES (?, ?, ?)
    ''', (name, description, now))
    
    sticker_id = c.lastrowid
    conn.commit()
    conn.close()
    return sticker_id

def add_sighting(sticker_id, latitude, longitude, image_path):
    """Add a new sticker sighting."""
    conn = get_db()
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT INTO sightings (sticker_id, latitude, longitude, image_path, spotted_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (sticker_id, latitude, longitude, image_path, now))
    
    sighting_id = c.lastrowid
    conn.commit()
    conn.close()
    return sighting_id

def update_wiki_content(sticker_id, content):
    """Update wiki content for a sticker."""
    conn = get_db()
    c = conn.cursor()
    now = datetime.now().isoformat()
    
    c.execute('''
        INSERT OR REPLACE INTO wiki_content (sticker_id, content, updated_at)
        VALUES (?, ?, ?)
    ''', (sticker_id, content, now))
    
    conn.commit()
    conn.close()

def get_sticker(sticker_id):
    """Get sticker details by ID."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM stickers WHERE id = ?', (sticker_id,))
    sticker = c.fetchone()
    
    conn.close()
    return dict(sticker) if sticker else None

def get_all_stickers():
    """Get all stickers."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM stickers ORDER BY created_at DESC')
    stickers = c.fetchall()
    
    conn.close()
    return [dict(sticker) for sticker in stickers]

def get_sticker_sightings(sticker_id):
    """Get all sightings for a sticker."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM sightings WHERE sticker_id = ? ORDER BY spotted_at DESC', (sticker_id,))
    sightings = c.fetchall()
    
    conn.close()
    return [dict(sighting) for sighting in sightings]

def get_wiki_content(sticker_id):
    """Get wiki content for a sticker."""
    conn = get_db()
    c = conn.cursor()
    
    c.execute('SELECT * FROM wiki_content WHERE sticker_id = ?', (sticker_id,))
    content = c.fetchone()
    
    conn.close()
    return dict(content) if content else None