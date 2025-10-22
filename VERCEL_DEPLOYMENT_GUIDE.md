# Vercel Deployment Guide for Luxury Car Rental Service

This guide explains how to deploy the Node.js version of the Luxury Car Rental Service to Vercel and add a custom domain.

## Prerequisites

1. A Vercel account (free at [vercel.com](https://vercel.com))
2. The Node.js version of the application (server.js)
3. A custom domain (optional but recommended)

## Files Added for Vercel Deployment

This project now includes several files to facilitate deployment to Vercel:

1. `vercel.json` - Vercel configuration file
2. `now.json` - Alternative configuration file (backward compatibility)
3. `index.js` - Entry point for the application
4. `VERCEL_DEPLOYMENT_GUIDE.md` - This guide

## Deploying to Vercel

### Method 1: Using Vercel CLI (Recommended)

1. Install Vercel CLI globally:
   ```bash
   npm install -g vercel
   ```

2. Log in to your Vercel account:
   ```bash
   vercel login
   ```

3. Deploy the project:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Set the project name (e.g., luxury-car-rental)
   - Select the default scope
   - Choose the directory (current directory)
   - Select "No" for framework preset
   - Set the output directory (leave as default)
   - Choose "Yes" for overriding existing deployment (if applicable)

### Method 2: Using Git Integration

1. Push your code to a Git repository (GitHub, GitLab, or Bitbucket)
2. Log in to your Vercel dashboard
3. Click "New Project"
4. Import your Git repository
5. Configure the project:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty - Vercel will auto-detect)
   - Output Directory: (leave empty)
6. Click "Deploy"

## Adding a Custom Domain

After your project is deployed:

1. In your Vercel dashboard, go to your project
2. Click on "Settings" tab
3. Click on "Domains" in the sidebar
4. Click "Add Domain"
5. Enter your custom domain (e.g., www.luxurycarrental.com)
6. Follow the DNS configuration instructions:

### DNS Configuration Options

#### Option 1: Using DNS Verification (Recommended)
- Add a TXT record to verify domain ownership
- Vercel will provide the specific TXT record values

#### Option 2: Using Nameservers
- Point your domain's nameservers to Vercel's nameservers
- Vercel will provide the nameserver addresses

#### Option 3: Using Alias (CNAME)
- Add a CNAME record pointing to your Vercel deployment URL
- For root domains, you may need to use ANAME or ALIAS records

## Environment Variables

If your application requires environment variables:

1. In your Vercel dashboard, go to your project
2. Click on "Settings" tab
3. Click on "Environment Variables" in the sidebar
4. Add your environment variables:
   - KEY: VARIABLE_NAME
   - VALUE: variable_value
   - ENVIRONMENT: Development, Preview, and/or Production

## Important Notes

1. **Framework Compatibility**: Vercel works best with Node.js applications. The Flask (Python) version of this application may not deploy correctly to Vercel.

2. **Database Considerations**: 
   - The application uses SQLite for data storage
   - For production deployments, consider using a managed database service
   - Environment variables can be used to configure database connections

3. **Static Assets**: 
   - Static files in the `static/` directory are automatically served
   - Images and other assets will be accessible via the deployed URL

4. **Port Configuration**: 
   - Vercel automatically handles port configuration
   - The application will be available on port 443 (HTTPS) or 80 (HTTP)

5. **Health Check Endpoint**: 
   - A `/health` endpoint has been added for monitoring purposes
   - Returns a JSON response with status "OK" and timestamp

## Troubleshooting

### Common Issues

1. **Deployment Failures**:
   - Check the build logs in your Vercel dashboard
   - Ensure all dependencies are listed in package.json
   - Verify the Node.js version compatibility

2. **Domain Not Resolving**:
   - Verify DNS records are correctly configured
   - DNS changes may take up to 48 hours to propagate
   - Use tools like `nslookup` or `dig` to verify DNS records

3. **Mixed Content Issues**:
   - Ensure all resources are loaded over HTTPS
   - Update any hardcoded HTTP URLs to use HTTPS or relative paths

### Support

For Vercel-specific issues, refer to the [Vercel documentation](https://vercel.com/docs) or contact their support team.

For application-specific issues, check the existing documentation files:
- [README.md](README.md)
- [NODEJS_README.md](NODEJS_README.md)
- [DOCUMENTATION.md](DOCUMENTATION.md)