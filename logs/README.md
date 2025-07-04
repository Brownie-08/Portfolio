# Logs Directory

This directory contains application logs for production deployment.

## Log Files

- `django.log` - Main application log file
- `error.log` - Error-specific logs
- `access.log` - Request access logs

## Log Rotation

Logs are automatically rotated by the deployment platform to prevent disk space issues.

## Monitoring

Monitor logs through:
- DigitalOcean App Platform Console
- Log aggregation services (optional)
- Custom monitoring solutions

**Note**: This directory is created automatically in production environments.
