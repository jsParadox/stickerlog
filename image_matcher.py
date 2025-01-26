import cv2
import numpy as np
import os
from pathlib import Path

class ImageMatcher:
    def __init__(self, stickers_dir='static/uploads/stickers'):
        """Initialize the image matcher with the directory containing sticker images."""
        self.stickers_dir = Path(stickers_dir)
        self.sift = cv2.SIFT_create()
        
    def _load_and_process_image(self, image_path):
        """Load and process an image for feature detection."""
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect features
        keypoints, descriptors = self.sift.detectAndCompute(gray, None)
        return keypoints, descriptors

    def find_matches(self, new_image_path, threshold=0.7):
        """
        Find matches for a new image among existing stickers.
        Returns a list of (sticker_id, match_score) tuples.
        """
        try:
            # Load and process the new image
            new_kp, new_desc = self._load_and_process_image(new_image_path)
            if new_desc is None:
                return []

            matches = []
            # Create feature matcher
            bf = cv2.BFMatcher()

            # Compare with each existing sticker
            for sticker_path in self.stickers_dir.glob('*.jpg'):
                try:
                    # Extract sticker ID from filename (assuming format: id_*.jpg)
                    sticker_id = int(sticker_path.stem.split('_')[0])
                    
                    # Load and process existing sticker
                    sticker_kp, sticker_desc = self._load_and_process_image(sticker_path)
                    if sticker_desc is None:
                        continue

                    # Find matches between descriptors
                    raw_matches = bf.knnMatch(new_desc, sticker_desc, k=2)
                    
                    # Apply ratio test
                    good_matches = []
                    for m, n in raw_matches:
                        if m.distance < threshold * n.distance:
                            good_matches.append(m)

                    # Calculate match score
                    match_score = len(good_matches) / min(len(new_kp), len(sticker_kp))
                    
                    if match_score > 0.1:  # Only include if there's a significant match
                        matches.append((sticker_id, match_score))

                except Exception as e:
                    print(f"Error processing sticker {sticker_path}: {e}")
                    continue

            # Sort by match score descending
            matches.sort(key=lambda x: x[1], reverse=True)
            return matches

        except Exception as e:
            print(f"Error in find_matches: {e}")
            return []

    def save_sticker_image(self, image_path, sticker_id):
        """
        Save a new sticker image with the given ID.
        Returns the path where the image was saved.
        """
        # Create stickers directory if it doesn't exist
        self.stickers_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and resize image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Resize if too large while maintaining aspect ratio
        max_size = 800
        height, width = img.shape[:2]
        if height > max_size or width > max_size:
            if height > width:
                new_height = max_size
                new_width = int(width * (max_size / height))
            else:
                new_width = max_size
                new_height = int(height * (max_size / width))
            img = cv2.resize(img, (new_width, new_height))
        
        # Save image with sticker ID in filename
        new_path = self.stickers_dir / f"{sticker_id}_sticker.jpg"
        cv2.imwrite(str(new_path), img)
        
        return str(new_path)

    def save_sighting_image(self, image_path, sighting_id, sightings_dir='static/uploads/sightings'):
        """
        Save a sighting image.
        Returns the path where the image was saved.
        """
        sightings_dir = Path(sightings_dir)
        sightings_dir.mkdir(parents=True, exist_ok=True)
        
        # Load and resize image
        img = cv2.imread(str(image_path))
        if img is None:
            raise ValueError(f"Could not load image: {image_path}")
        
        # Resize if too large while maintaining aspect ratio
        max_size = 800
        height, width = img.shape[:2]
        if height > max_size or width > max_size:
            if height > width:
                new_height = max_size
                new_width = int(width * (max_size / height))
            else:
                new_width = max_size
                new_height = int(height * (max_size / width))
            img = cv2.resize(img, (new_width, new_height))
        
        # Save image with sighting ID in filename
        new_path = sightings_dir / f"{sighting_id}_sighting.jpg"
        cv2.imwrite(str(new_path), img)
        
        return str(new_path)