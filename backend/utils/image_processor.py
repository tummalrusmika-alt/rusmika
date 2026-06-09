import cv2
import numpy as np
from PIL import Image
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Process and verify images for complaint reports
    """
    
    @staticmethod
    def verify_image_authenticity(image_path: str) -> dict:
        """
        Verify image authenticity and extract features
        Returns: {
            is_authentic: bool,
            confidence: float,
            detected_objects: list,
            image_quality: str
        }
        """
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                return {
                    "is_authentic": False,
                    "confidence": 0.0,
                    "detected_objects": [],
                    "error": "Could not read image"
                }
            
            # Check image quality
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            variance = laplacian.var()
            
            quality = "high" if variance > 100 else "medium" if variance > 50 else "low"
            
            # Basic object detection (potholes, garbage, streetlights)
            detected_objects = ImageProcessor._detect_objects(image)
            
            # Authenticity check (basic)
            is_authentic = len(detected_objects) > 0 or quality in ["high", "medium"]
            confidence = min(0.95, 0.5 + (len(detected_objects) * 0.15) + (variance / 500))
            
            return {
                "is_authentic": is_authentic,
                "confidence": min(confidence, 1.0),
                "detected_objects": detected_objects,
                "image_quality": quality,
                "blur_variance": float(variance)
            }
            
        except Exception as e:
            logger.error(f"Error verifying image: {str(e)}")
            return {
                "is_authentic": False,
                "confidence": 0.0,
                "detected_objects": [],
                "error": str(e)
            }
    
    @staticmethod
    def _detect_objects(image) -> list:
        """
        Detect common complaint objects (potholes, garbage, broken lights)
        Simple feature detection using edge detection
        """
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            detected = []
            
            if len(contours) > 5:
                detected.append("pothole")  # Many edges indicate surface damage
            
            # Check for dark areas (garbage)
            dark_pixels = np.sum(gray < 100)
            if dark_pixels > (gray.size * 0.2):
                detected.append("debris_or_garbage")
            
            # Check for circular objects (streetlights)
            for contour in contours[-5:]:  # Check top 5 contours
                area = cv2.contourArea(contour)
                if area > 100:
                    x, y, w, h = cv2.boundingRect(contour)
                    aspect_ratio = float(w) / h if h != 0 else 0
                    if 0.8 < aspect_ratio < 1.2:
                        detected.append("light_fixture")
                        break
            
            return list(set(detected))
            
        except Exception as e:
            logger.error(f"Error detecting objects: {str(e)}")
            return []
    
    @staticmethod
    def calculate_severity_score(
        image_path: str,
        category: str,
        description: str = ""
    ) -> float:
        """
        Calculate severity score for complaint (0.0 to 1.0)
        """
        try:
            score = 0.0
            
            # Image quality score (0-0.3)
            verification = ImageProcessor.verify_image_authenticity(image_path)
            score += verification["confidence"] * 0.3
            
            # Category-based score (0-0.3)
            category_scores = {
                "pothole": 0.8,
                "garbage": 0.6,
                "streetlight": 0.7,
                "flooding": 0.9,
                "road_damage": 0.85,
                "other": 0.5
            }
            score += category_scores.get(category.lower(), 0.5) * 0.3
            
            # Description complexity (0-0.4)
            desc_score = min(len(description.split()) / 50, 1.0)
            score += desc_score * 0.4
            
            return min(score, 1.0)
            
        except Exception as e:
            logger.error(f"Error calculating severity score: {str(e)}")
            return 0.5
    
    @staticmethod
    def save_image(image_bytes, filename: str) -> str:
        """
        Save uploaded image and return file path
        """
        try:
            os.makedirs("uploads", exist_ok=True)
            filepath = os.path.join("uploads", filename)
            
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            
            logger.info(f"Image saved: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            return None
    
    @staticmethod
    def compare_images(image1_path: str, image2_path: str) -> float:
        """
        Compare two images for similarity (0.0 to 1.0)
        Used for duplicate detection
        """
        try:
            img1 = cv2.imread(image1_path)
            img2 = cv2.imread(image2_path)
            
            if img1 is None or img2 is None:
                return 0.0
            
            # Resize images to same size
            height, width = min(img1.shape[0], img2.shape[0]), min(img1.shape[1], img2.shape[1])
            img1 = cv2.resize(img1, (width, height))
            img2 = cv2.resize(img2, (width, height))
            
            # Calculate similarity
            difference = cv2.subtract(img1, img2)
            b, g, r = cv2.split(difference)
            
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                return 1.0
            
            # Calculate MSSIM for more accurate comparison
            mse = np.sum((img1.astype(float) - img2.astype(float)) ** 2) / (height * width * 3)
            similarity = np.exp(-mse / 10000)
            
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error comparing images: {str(e)}")
            return 0.0
