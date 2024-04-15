import piexif

def add_tag_to_image(image_path, tag):
    try:
        # Load existing EXIF data from the image
        exif_data = piexif.load(image_path)
        
        # Get the existing tags from the EXIF data
        existing_tags_bytes = exif_data['0th'].get(piexif.ImageIFD.XPKeywords, b'')
        if isinstance(existing_tags_bytes, bytes):
            existing_tags = existing_tags_bytes.decode('utf-8')
        else:
            existing_tags = ''
        
        # Append the new tag to the existing tags
        updated_tags = existing_tags + (', ' if existing_tags else '') + tag
        
        # Encode the updated tags as bytes
        updated_tags_bytes = updated_tags.encode('utf-16le')
        
        # Update the EXIF data with the updated tags
        exif_data['0th'][piexif.ImageIFD.XPKeywords] = updated_tags_bytes
        
        # Convert the EXIF data back to binary format
        exif_bytes = piexif.dump(exif_data)
        
        # Save the modified EXIF data back to the image
        piexif.insert(exif_bytes, image_path)
        
        print(f"Tag 'test' added successfully to {image_path}")
    except Exception as e:
        print(f"Error adding tag to {image_path}: {e}")

def main():
    image_path = "C:/Users/joela/Desktop/test/98508485_p0_master1200.jpg"  # Adjust this path to your image file
    
    add_tag_to_image(image_path, "test")

if __name__ == "__main__":
    main()
