# 🚀 MD2PDF Fly.io Deployment Guide

This guide will help you deploy MD2PDF to Fly.io with full Docker support, enabling all LaTeX templates including the Official Eisvogel template.

## Prerequisites

1. **Fly.io Account**: Sign up at [fly.io](https://fly.io)
2. **Fly CLI**: Install the flyctl command line tool
3. **Docker**: For local testing (optional)

## Installation Steps

### 1. Install Fly CLI

**macOS:**
```bash
curl -L https://fly.io/install.sh | sh
```

**Windows:**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Linux:**
```bash
curl -L https://fly.io/install.sh | sh
```

### 2. Login to Fly.io

```bash
flyctl auth login
```

### 3. Clone and Prepare Project

```bash
# If you haven't already, clone your project
git clone <your-repo-url>
cd md2pdf

# Verify all files are present
ls -la
# You should see: app.py, Dockerfile, fly.toml, eisvogel.latex, docs/
```

## Deployment Process

### 1. Launch the App

```bash
# Create and deploy the app (first time)
flyctl launch

# Follow the prompts:
# - App name: md2pdf (or your preferred name)
# - Region: Choose closest to your users
# - Database: No
# - Deploy now: Yes
```

### 2. Alternative: Deploy Existing Configuration

If you already have the `fly.toml` file:

```bash
# Deploy using existing configuration
flyctl deploy
```

### 3. Monitor Deployment

```bash
# Check deployment status
flyctl status

# View logs
flyctl logs

# Monitor health
flyctl checks list
```

## Configuration Details

### Resources (fly.toml)

Current configuration:
- **CPU**: 1 shared vCPU
- **Memory**: 1GB RAM
- **Auto-scaling**: Enabled (0-1 machines)
- **Region**: Frankfurt (fra) - change as needed

### Environment Variables

The app is configured with:
- `PORT=8501` (Streamlit default)
- `PYTHONUNBUFFERED=1`
- `PYTHONDONTWRITEBYTECODE=1`

## Template Support

With Fly.io deployment, all templates are fully supported:

### ✅ Enhanced Custom Template
- Default and recommended
- Gray code blocks with professional styling
- Optimized for reliability

### ✅ Official Eisvogel Template  
- Full professional LaTeX template
- Source Sans Pro and Source Code Pro fonts
- Advanced typography features
- **Now works with Docker deployment!**

### ✅ Basic Fallback Template
- Simple, minimal styling
- Maximum compatibility

## Scaling and Performance

### Scale Up for Heavy Usage

```bash
# Increase memory for large documents
flyctl scale memory 2048

# Add more CPU cores
flyctl scale vm shared-cpu-2x

# Set minimum running machines
flyctl scale count 1
```

### Cost Optimization

```bash
# Scale down for cost savings
flyctl scale memory 512
flyctl scale count 0  # Auto-sleep when not in use
```

## Monitoring and Maintenance

### View Application Logs

```bash
# Real-time logs
flyctl logs

# Historical logs
flyctl logs --since=1h
```

### Health Checks

The app includes built-in health checks:
- **Endpoint**: `/_stcore/health`
- **Interval**: 30 seconds
- **Timeout**: 10 seconds

### Updates and Redeployment

```bash
# Deploy changes
git add .
git commit -m "Update MD2PDF"
flyctl deploy

# Force rebuild (if needed)
flyctl deploy --no-cache
```

## Troubleshooting

### Common Issues

1. **Build Failures**
   ```bash
   # Check build logs
   flyctl logs --app md2pdf
   
   # Retry with verbose output
   flyctl deploy --verbose
   ```

2. **Memory Issues**
   ```bash
   # Increase memory allocation
   flyctl scale memory 2048
   ```

3. **LaTeX Package Issues**
   ```bash
   # Check if LaTeX packages are installed
   flyctl ssh console
   # Inside container:
   tlmgr list --installed | grep source
   ```

### DNS and Custom Domains

```bash
# Add custom domain
flyctl certs create yourdomain.com

# Check certificate status
flyctl certs show yourdomain.com
```

## Security Considerations

- App runs as non-root user (appuser)
- HTTPS enforced by default
- Health checks for reliability
- Automatic security updates via base image

## Cost Estimation

**Basic Usage (Free Tier)**:
- 1 shared vCPU, 1GB RAM
- ~$0-5/month with moderate usage
- Free allowance covers most personal usage

**Heavy Usage**:
- 2 shared vCPUs, 2GB RAM  
- ~$10-20/month
- Suitable for team/production use

## Next Steps

1. **Test the deployment**: Visit your app URL
2. **Try all templates**: Verify Official Eisvogel works
3. **Upload test files**: Confirm PDF generation
4. **Set up monitoring**: Configure alerts if needed
5. **Custom domain**: Add your domain if desired

## Support

- **Fly.io Docs**: https://fly.io/docs/
- **MD2PDF Issues**: Create GitHub issue
- **Community**: Fly.io community forum

Your MD2PDF app is now deployed with full Docker flexibility! 🎉