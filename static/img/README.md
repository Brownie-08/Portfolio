# Images Directory

This directory contains static images for the portfolio website.

## Structure

- `projects/` - Project screenshots and images
- `blog/` - Blog post images and thumbnails
- `icons/` - Site icons and logos
- `backgrounds/` - Background images and patterns

## Recommended File Formats

- **Photos**: JPEG (.jpg)
- **Graphics with transparency**: PNG (.png)
- **Icons**: SVG (.svg) or PNG
- **Favicons**: ICO (.ico)

## Image Optimization

For best performance:
- Compress images before uploading
- Use appropriate dimensions (don't rely on CSS scaling)
- Consider using WebP format for modern browsers
- Provide alt text for accessibility

## Example Usage

```html
<img src="{% static 'img/projects/project1.jpg' %}" alt="Project 1 Screenshot" class="img-fluid">
```
