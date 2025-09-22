# Alanube Python API Documentation

This directory contains the comprehensive documentation for the Alanube Python API client, built with Jekyll and deployed to GitHub Pages.

## 📚 Documentation Structure

```
docs/
├── _config.yml              # Jekyll configuration
├── _layouts/
│   └── default.html         # Default page layout
├── assets/
│   └── favicon.ico          # Site favicon
├── index.md                 # Home page
├── installation.md          # Installation guide
├── usage.md                 # Usage examples
├── countries.md             # Country support guide
├── contributing.md          # Contributing guide
└── README.md               # This file
```

## 🚀 Quick Start

### Local Development

1. **Install Jekyll:**
   ```bash
   # On macOS
   brew install ruby
   gem install jekyll bundler

   # On Ubuntu/Debian
   sudo apt install ruby-full build-essential
   gem install jekyll bundler

   # On Windows
   # Download Ruby from rubyinstaller.org
   gem install jekyll bundler
   ```

2. **Serve Locally:**
   ```bash
   cd docs
   jekyll serve
   ```

3. **View Documentation:**
   Open http://localhost:4000 in your browser

### Building for Production

```bash
cd docs
jekyll build
```

The built site will be in `docs/_site/`.

## 📝 Adding New Documentation

### Creating a New Page

1. **Create a new Markdown file:**
   ```bash
   touch docs/new-page.md
   ```

2. **Add front matter:**
   ```markdown
   ---
   title: New Page Title
   description: Brief description of the page
   ---

   # New Page Title

   Your content here...
   ```

3. **Add to navigation:**
   Edit `docs/_config.yml` and add to the `nav` section:
   ```yaml
   nav:
     - title: New Page
       url: /new-page/
   ```

### Documentation Guidelines

1. **Use Clear Headings:**
   ```markdown
   # Main Title
   ## Section Title
   ### Subsection Title
   ```

2. **Include Code Examples:**
   ```markdown
   ```python
   from alanube.do import Alanube

   Alanube.connect("token", developer_mode=True)
   ```
   ```

3. **Add Tables for Reference:**
   ```markdown
   | Column 1 | Column 2 |
   |----------|----------|
   | Value 1  | Value 2  |
   ```

4. **Use Alerts for Important Information:**
   ```markdown
   > **Note:** Important information here.

   > **Warning:** Warning message here.

   > **Tip:** Helpful tip here.
   ```

## 🎨 Customization

### Styling

The documentation uses Bootstrap 5 and custom CSS. To modify styles:

1. **Edit the layout file:** `docs/_layouts/default.html`
2. **Add custom CSS:** In the `<style>` section
3. **Use Bootstrap classes:** For responsive design

### Configuration

Edit `docs/_config.yml` to customize:

- Site title and description
- Navigation menu
- Social media links
- Build settings
- Plugin configuration

## 🔧 Deployment

### GitHub Pages

The documentation is automatically deployed to GitHub Pages when changes are pushed to the main branch.

**Manual Deployment:**
1. Push changes to the main branch
2. GitHub Actions will build and deploy automatically
3. Check the Actions tab for build status

### Custom Domain

To use a custom domain:

1. **Add CNAME file:**
   ```bash
   echo "your-domain.com" > docs/CNAME
   ```

2. **Update configuration:**
   Edit `docs/_config.yml`:
   ```yaml
   url: "https://your-domain.com"
   baseurl: ""
   ```

3. **Configure DNS:**
   Point your domain to GitHub Pages

## 📊 Analytics

### Google Analytics

To add Google Analytics:

1. **Get tracking ID** from Google Analytics
2. **Update configuration:**
   ```yaml
   # In _config.yml
   google_analytics: UA-XXXXXXXXX-X
   ```

3. **Add tracking code** to the layout file

### Search Console

1. **Verify ownership** in Google Search Console
2. **Submit sitemap:** `https://your-domain.com/sitemap.xml`

## 🐛 Troubleshooting

### Common Issues

1. **Build Errors:**
   ```bash
   # Check Jekyll version
   jekyll --version

   # Clean and rebuild
   jekyll clean
   jekyll build
   ```

2. **Missing Dependencies:**
   ```bash
   # Install missing gems
   bundle install
   ```

3. **Local Server Issues:**
   ```bash
   # Use different port
   jekyll serve --port 4001

   # Bind to all interfaces
   jekyll serve --host 0.0.0.0
   ```

### Debug Mode

```bash
# Enable debug output
jekyll serve --verbose
```

## 🤝 Contributing

### Documentation Standards

1. **Write clearly** and concisely
2. **Include examples** for all features
3. **Test code examples** before committing
4. **Use proper Markdown** formatting
5. **Add links** to related pages

### Review Process

1. **Create a branch** for your changes
2. **Test locally** before submitting
3. **Submit a pull request** with description
4. **Wait for review** and address feedback

### Style Guide

- **Headings:** Use sentence case
- **Code:** Use syntax highlighting
- **Links:** Use descriptive text
- **Images:** Include alt text
- **Tables:** Include headers

## 📞 Support

For documentation issues:

1. **Check existing issues** on GitHub
2. **Create a new issue** with details
3. **Contact the maintainers** if urgent

## 📄 License

This documentation is licensed under the same license as the main project (MIT).

---

**Happy documenting! 📚✨**