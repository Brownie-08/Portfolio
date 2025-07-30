# 🚀 Cloudinary Setup Guide for Production

This guide will walk you through setting up Cloudinary for your portfolio website to fix the broken image issue on Render.

## 1. Sign up for Cloudinary (Free)
- Go to: https://cloudinary.com/users/register/free
- Complete the registration to create your free account.

## 2. Get Your Cloudinary Credentials
- Go to your Cloudinary dashboard: https://cloudinary.com/console
- Find your **Cloud Name**, **API Key**, and **API Secret**.

## 3. Add Environment Variables to Render
- Go to your Render dashboard: https://dashboard.render.com
- Find your portfolio service and go to the **Environment** tab.
- Add the following secret files with the values from your Cloudinary dashboard:

| Key                     | Value                  |
|-------------------------|------------------------|
| `USE_CLOUDINARY`        | `True`                 |
| `CLOUDINARY_CLOUD_NAME` | Your Cloudinary cloud name |
| `CLOUDINARY_API_KEY`    | Your Cloudinary API key    |
| `CLOUDINARY_API_SECRET` | Your Cloudinary API secret |

## 4. Redeploy Your Application
- Go to your Render dashboard.
- Manually trigger a new deployment for your portfolio service.

That's it! After redeploying, your images will be uploaded to Cloudinary, and they will persist across all future deployments.

