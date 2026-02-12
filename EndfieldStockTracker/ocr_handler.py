"""
OCR module for extracting prices from screenshots
Handles image processing and text recognition
"""
from PIL import ImageGrab, Image, ImageTk
import numpy as np
import re
from typing import List, Tuple, Optional


class PriceOCR:
    def __init__(self):
        self.tesseract_available = False
        self.easyocr_available = False
        self.reader = None
        self.import_errors = []
        self.easyocr_module = None
        
        # Try to import OCR libraries (but don't initialize yet)
        try:
            import pytesseract
            self.tesseract_available = True
            self.pytesseract = pytesseract
        except ImportError as e:
            self.import_errors.append(f"Tesseract: {str(e)}")
        except Exception as e:
            self.import_errors.append(f"Tesseract error: {str(e)}")
        
        # Check if EasyOCR is importable (but don't initialize the Reader yet)
        try:
            import easyocr
            self.easyocr_available = True
            self.easyocr_module = easyocr
        except ImportError as e:
            self.import_errors.append(f"EasyOCR: {str(e)}")
        except Exception as e:
            self.import_errors.append(f"EasyOCR error: {str(e)}")
    
    def is_available(self) -> Tuple[bool, str]:
        """Check if OCR is available"""
        if self.easyocr_available:
            return True, "easyocr"
        elif self.tesseract_available:
            return True, "tesseract"
        else:
            return False, "none"
    
    def get_error_messages(self) -> str:
        """Get detailed error messages about import failures"""
        if not self.import_errors:
            return "No errors"
        return "\n".join(self.import_errors)
    
    def get_clipboard_image(self) -> Optional[Image.Image]:
        """Get image from clipboard"""
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                return image
            return None
        except Exception as e:
            print(f"Error getting clipboard image: {e}")
            return None
    
    def extract_numbers(self, image: Image.Image) -> List[int]:
        """Extract all numbers from image using OCR"""
        if self.easyocr_available:
            # Initialize reader on first use (lazy loading)
            if self.reader is None:
                print("Initializing EasyOCR (this may take a moment on first use)...")
                self.reader = self.easyocr_module.Reader(['en'], gpu=False)
            return self._extract_with_easyocr(image)
        elif self.tesseract_available:
            return self._extract_with_tesseract(image)
        else:
            return []
    
    def _extract_with_easyocr(self, image: Image.Image) -> List[int]:
        """Extract numbers using EasyOCR"""
        try:
            # Convert PIL Image to numpy array
            image_np = np.array(image)
            
            results = self.reader.readtext(image_np)
            numbers = []
            
            for detection in results:
                text = detection[1]
                # Extract numbers from text
                found_numbers = re.findall(r'\d+', text)
                for num_str in found_numbers:
                    try:
                        num = int(num_str)
                        # Filter reasonable prices (between 100 and 10000)
                        if 100 <= num <= 10000:
                            numbers.append(num)
                    except ValueError:
                        continue
            
            return numbers
        except Exception as e:
            print(f"Error with EasyOCR: {e}")
            return []
    
    def _extract_with_tesseract(self, image: Image.Image) -> List[int]:
        """Extract numbers using Tesseract"""
        try:
            # Configure tesseract for better number recognition
            config = '--psm 6 digits'
            text = self.pytesseract.image_to_string(image, config=config)
            
            numbers = []
            # Extract all numbers from text
            found_numbers = re.findall(r'\d+', text)
            
            for num_str in found_numbers:
                try:
                    num = int(num_str)
                    # Filter reasonable prices (between 100 and 10000)
                    if 100 <= num <= 10000:
                        numbers.append(num)
                except ValueError:
                    continue
            
            return numbers
        except Exception as e:
            print(f"Error with Tesseract: {e}")
            return []
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        # Convert to grayscale
        image = image.convert('L')
        
        # Optional: enhance contrast
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        return image
