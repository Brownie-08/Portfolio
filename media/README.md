# Media Directory

This directory contains user-uploaded files and dynamic media content.

## Structure

- `projects/` - Project images uploaded via admin
- `blog/` - Blog post images and attachments
- `uploads/` - General file uploads
- `cache/` - Thumbnail cache (if using image processing)

## Security Considerations

- All uploaded files should be validated
- Implement file type restrictions
- Consider virus scanning for uploads
- Use secure file naming conventions
- Regular cleanup of temporary files

## File Handling

Django settings control:
- `MEDIA_URL` - URL prefix for serving media files
- `MEDIA_ROOT` - File system path to media files
- File upload size limits
- Allowed file extensions

## Production Notes

For production deployment:
- Consider using cloud storage (AWS S3, CloudFront)
- Implement proper backup strategies
- Monitor disk usage
- Use CDN for better performance

## Example Model Usage

```python
class Project(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
```
