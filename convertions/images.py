from PIL import Image
import os

def convert_image(input_path, output_path, target_format):
    try:
        img = Image.open(input_path)

        # Ensure proper format for output file extension
        target_format = target_format.lower()
        valid_formats = ['jpeg', 'jpg', 'png', 'bmp', 'gif', 'tiff', 'webp']
        
        if target_format not in valid_formats:
            raise ValueError(f"Unsupported target format: {target_format}")

        # Handle transparency issues when converting RGBA to JPG
        if img.mode == 'RGBA' and target_format in ['jpg', 'jpeg']:
            background = Image.new('RGB', img.size, (255, 255, 255))  # White background
            img = Image.alpha_composite(background, img.convert('RGBA')).convert('RGB')

        elif img.mode != 'RGB' and target_format in ['jpg', 'jpeg']:
            img = img.convert('RGB')

        # Save with appropriate format
        img.save(output_path, format=target_format.upper())
        print(f"Successfully converted {input_path} to {output_path}")

    except Exception as e:
        print(f"Conversion failed: {e}")

