# API Documentation for Luxury Car Rental Service

This document describes the available API endpoints for the Node.js version of the Luxury Car Rental Service, which can be useful for monitoring and testing when deployed on Vercel.

## Health Check Endpoint

### GET /health

Returns the health status of the application.

**Response:**
```json
{
  "status": "OK",
  "timestamp": "2023-10-22T10:00:00.000Z"
}
```

**HTTP Status Codes:**
- 200: Application is running properly

## Web Pages

### GET /

Returns the login page.

### GET /dashboard

Returns the main dashboard with available luxury cars.

### GET /logout

Redirects to the home page.

## Monitoring

When deployed on Vercel, you can monitor your application using:

1. Vercel Dashboard - Check deployments, logs, and performance
2. Health endpoint - Use the `/health` endpoint for uptime monitoring
3. Vercel Analytics - Built-in analytics for page views and performance

## Testing Endpoints

After deployment, you can test the endpoints using:

1. Browser navigation to the URLs
2. curl commands:
   ```bash
   curl https://your-domain.vercel.app/health
   ```
3. Postman or similar API testing tools

## Custom Domain Access

Once you've added a custom domain to your Vercel deployment, you can access your application at:

- https://your-custom-domain.com/
- https://www.your-custom-domain.com/

The API endpoints will be available at the same domain:

- https://your-custom-domain.com/health