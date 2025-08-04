# Alanube Python API - Documentation Setup Guide

This document provides a complete overview of the documentation setup for the Alanube Python API project, including installation, usage, and deployment instructions.

## 📋 Overview

The documentation for the Alanube Python API has been set up using:

- **Jekyll** - Static site generator
- **GitHub Pages** - Hosting platform
- **Bootstrap 5** - CSS framework
- **GitHub Actions** - Automated deployment

## 🏗️ Documentation Structure

```
docs/
├── _config.yml              # Jekyll site configuration
├── _layouts/
│   └── default.html         # Main page layout template
├── assets/
│   └── favicon.ico          # Site favicon (placeholder)
├── index.md                 # Home page with overview
├── installation.md          # Installation guide
├── usage.md                 # Usage examples and tutorials
├── api-reference.md         # Complete API reference
├── countries.md             # Country-specific features
├── contributing.md          # Contributing guidelines
├── troubleshooting.md       # Common issues and solutions
├── README.md               # Documentation development guide
└── Gemfile                 # Jekyll dependencies

.github/workflows/
└── docs.yml                # GitHub Actions deployment workflow
```

## 🚀 Quick Start

### 1. Enable GitHub Pages

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Pages**
3. Under **Source**, select **GitHub Actions**
4. The workflow will automatically deploy when you push to main branch

### 2. Local Development

```bash
# Install Ruby and Jekyll
# On macOS:
brew install ruby
gem install jekyll bundler

# On Ubuntu/Debian:
sudo apt install ruby-full build-essential
gem install jekyll bundler

# On Windows:
# Download Ruby from rubyinstaller.org
gem install jekyll bundler

# Install dependencies
cd docs
bundle install

# Serve locally
bundle exec jekyll serve
```

3. Open http://localhost:4000 in your browser

## 📚 Documentation Content

### 1. Home Page (`index.md`)
- Project overview and quick start
- Feature highlights
- Supported countries
- Document types table
- Links to all sections

### 2. Installation Guide (`installation.md`)
- Prerequisites
- Installation methods (PyPI, source)
- Environment setup
- API token configuration
- Troubleshooting common installation issues

### 3. Usage Examples (`usage.md`)
- Basic setup and connection
- Company management
- Document sending (all types)
- Document retrieval and listing
- Cancellations and received documents
- Status checking
- Error handling examples
- Best practices

### 4. API Reference (`api-reference.md`)
- Complete method documentation
- Parameter descriptions
- Return types
- Error handling
- Data types
- Rate limiting information
- Best practices

### 5. Country Support (`countries.md`)
- Detailed country-specific information
- Dominican Republic (DGII) implementation
- Planned countries (Panama, Costa Rica, Peru, Bolivia)
- Tax systems and requirements
- Document numbering systems
- Implementation guidelines

### 6. Contributing Guide (`contributing.md`)
- Development setup
- Code style guidelines
- Testing procedures
- Documentation standards
- Pull request process
- Issue reporting templates

### 7. Troubleshooting (`troubleshooting.md`)
- Common installation issues
- Authentication problems
- API connection issues
- Validation errors
- Performance problems
- Country-specific issues
- Getting help

## 🎨 Customization

### Styling

The documentation uses a custom Bootstrap 5 theme with:

- **Color Scheme:**
  - Primary: Blue (#2563eb)
  - Secondary: Gray (#64748b)
  - Accent: Orange (#f59e0b)
  - Text: Dark gray (#1e293b)

- **Features:**
  - Responsive design
  - Syntax highlighting
  - Copy-to-clipboard buttons
  - Search functionality
  - Mobile-friendly navigation

### Configuration

Edit `docs/_config.yml` to customize:

```yaml
# Site information
title: "Alanube Python API Documentation"
description: "Comprehensive documentation for the Alanube Python API client"
url: "https://wilmerm.github.io/alanube-python"

# Navigation
nav:
  - title: Home
    url: /
  - title: Installation
    url: /installation/

# Social links
social:
  github: wilmerm/alanube-python
  twitter: AlanubeRD
```

## 🔧 Deployment

### Automatic Deployment

The documentation is automatically deployed via GitHub Actions:

1. **Trigger:** Push to main/master branch
2. **Build:** Jekyll builds the site
3. **Deploy:** Site is deployed to GitHub Pages
4. **URL:** https://wilmerm.github.io/alanube-python/

### Manual Deployment

```bash
# Build the site
cd docs
bundle exec jekyll build

# The built site is in _site/
# Upload to your hosting provider
```

### Custom Domain

To use a custom domain:

1. **Add CNAME file:**
   ```bash
   echo "docs.alanube.co" > docs/CNAME
   ```

2. **Update configuration:**
   ```yaml
   # In _config.yml
   url: "https://docs.alanube.co"
   baseurl: ""
   ```

3. **Configure DNS:**
   Point your domain to GitHub Pages

## 📊 Analytics and SEO

### Google Analytics

Add analytics tracking:

```yaml
# In _config.yml
google_analytics: UA-XXXXXXXXX-X
```

### SEO Optimization

The site includes:

- Meta tags for social sharing
- Open Graph tags
- Twitter Card tags
- Sitemap generation
- Structured data

## 🐛 Troubleshooting

### Common Issues

1. **Build Failures:**
   ```bash
   # Check Jekyll version
   jekyll --version

   # Clean and rebuild
   bundle exec jekyll clean
   bundle exec jekyll build
   ```

2. **Missing Dependencies:**
   ```bash
   # Install missing gems
   bundle install
   ```

3. **Local Server Issues:**
   ```bash
   # Use different port
   bundle exec jekyll serve --port 4001
   ```

### Debug Mode

```bash
# Enable verbose output
bundle exec jekyll serve --verbose
```

## 🤝 Contributing to Documentation

### Adding New Content

1. **Create new page:**
   ```bash
   touch docs/new-page.md
   ```

2. **Add front matter:**
   ```markdown
   ---
   title: Page Title
   description: Page description
   ---
   ```

3. **Update navigation:**
   Edit `docs/_config.yml` nav section

### Documentation Standards

- Use clear, concise language
- Include code examples
- Test all code snippets
- Use proper Markdown formatting
- Add links to related pages
- Include screenshots when helpful

### Review Process

1. Create a feature branch
2. Make your changes
3. Test locally
4. Submit a pull request
5. Wait for review and approval

## 📈 Maintenance

### Regular Tasks

1. **Update Dependencies:**
   ```bash
   bundle update
   ```

2. **Check for Broken Links:**
   ```bash
   bundle exec htmlproofer _site
   ```

3. **Update Content:**
   - Keep examples current
   - Update API documentation
   - Add new features
   - Fix reported issues

### Version Updates

When updating the library:

1. Update installation instructions
2. Review and update examples
3. Update API reference
4. Test all code snippets
5. Update version numbers

## 🎯 Best Practices

### Content Organization

- Use clear, descriptive headings
- Group related information
- Provide navigation between sections
- Include table of contents for long pages

### Code Examples

- Use realistic examples
- Include error handling
- Show both simple and complex use cases
- Test all code before committing

### User Experience

- Make information easy to find
- Use consistent formatting
- Provide multiple ways to access content
- Include search functionality

## 📞 Support

For documentation issues:

1. **Check existing issues** on GitHub
2. **Create a new issue** with details
3. **Contact maintainers** if urgent

## 🎉 Success Metrics

Track documentation success with:

- **Page views** and **time on page**
- **Search queries** and **click-through rates**
- **User feedback** and **issue reports**
- **Contribution frequency**
- **Support ticket reduction**

## 📄 License

This documentation is licensed under the MIT License, same as the main project.

---

**The documentation is now ready to help users effectively use the Alanube Python API! 🚀**

For questions or improvements, please open an issue or submit a pull request.