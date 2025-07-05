#!/usr/bin/env python3
"""
Script to create a placeholder certificate image
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_certificate_placeholder():
    # Create a certificate-like image
    width, height = 800, 600
    
    # Create a white background
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)
    
    # Draw a border
    border_color = '#2E7D32'  # Green
    border_width = 10
    draw.rectangle([border_width, border_width, width-border_width, height-border_width], 
                   outline=border_color, width=border_width)
    
    # Draw inner decorative border
    inner_border = 30
    draw.rectangle([inner_border, inner_border, width-inner_border, height-inner_border], 
                   outline=border_color, width=2)
    
    # Try to use a basic font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("arial.ttf", 48)
        subtitle_font = ImageFont.truetype("arial.ttf", 32)
        text_font = ImageFont.truetype("arial.ttf", 24)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()
    
    # Draw certificate text
    # Title
    title = "CERTIFICATE"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 80), title, fill=border_color, font=title_font)
    
    # Subtitle
    subtitle = "of Achievement"
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, 140), subtitle, fill='#666666', font=subtitle_font)
    
    # Main text
    main_text = "This certifies that"
    main_bbox = draw.textbbox((0, 0), main_text, font=text_font)
    main_width = main_bbox[2] - main_bbox[0]
    main_x = (width - main_width) // 2
    draw.text((main_x, 220), main_text, fill='#333333', font=text_font)
    
    # Name placeholder
    name = "Peter Emmanuel"
    name_bbox = draw.textbbox((0, 0), name, font=subtitle_font)
    name_width = name_bbox[2] - name_bbox[0]
    name_x = (width - name_width) // 2
    draw.text((name_x, 270), name, fill='#1976D2', font=subtitle_font)
    
    # Completion text
    completion_text = "has successfully completed"
    completion_bbox = draw.textbbox((0, 0), completion_text, font=text_font)
    completion_width = completion_bbox[2] - completion_bbox[0]
    completion_x = (width - completion_width) // 2
    draw.text((completion_x, 330), completion_text, fill='#333333', font=text_font)
    
    # Course name
    course = "Full Stack Web Development"
    course_bbox = draw.textbbox((0, 0), course, font=subtitle_font)
    course_width = course_bbox[2] - course_bbox[0]
    course_x = (width - course_width) // 2
    draw.text((course_x, 380), course, fill=border_color, font=subtitle_font)
    
    # Date and organization
    date_org = "May 2024 • Uptech Academy"
    date_bbox = draw.textbbox((0, 0), date_org, font=text_font)
    date_width = date_bbox[2] - date_bbox[0]
    date_x = (width - date_width) // 2
    draw.text((date_x, 460), date_org, fill='#666666', font=text_font)
    
    # Create directory if it doesn't exist
    os.makedirs('media/images/certifications', exist_ok=True)
    
    # Save the image
    output_path = 'media/images/certifications/fullstack_certificate.jpg'
    img.save(output_path, 'JPEG', quality=90)
    print(f"Certificate placeholder created: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_certificate_placeholder()
