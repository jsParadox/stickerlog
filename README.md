# Sticker Matcher Application

This is a Flask application that helps match and track sticker sightings.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

## Installation Instructions for macOS

1. Open Terminal and clone this repository:
   ```bash
   git clone <repository-url>
   cd stickers
   ```

2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated:
   ```bash
   source venv/bin/activate
   ```

2. Start the Flask application:
   ```bash
   python app.py
   ```

3. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Project Structure

- `/static` - Contains CSS, JavaScript, and uploaded images
- `/templates` - HTML templates
- `app.py` - Main Flask application
- `database.py` - Database operations
- `image_matcher.py` - Image matching functionality

## Notes

- The application stores uploaded images in `/static/uploads/`
- The SQLite database file is created automatically on first run
- Make sure to activate the virtual environment every time you work on the project

## Troubleshooting

If you encounter permission issues with the uploads directory:
```bash
chmod -R 755 static/uploads
```

If the application fails to start, ensure:
1. Virtual environment is activated
2. All dependencies are installed
3. Port 5000 is not in use by another application