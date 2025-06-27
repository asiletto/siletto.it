# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is Alessandro Siletto's personal website built with MkDocs using a custom theme called "mkdocs-simple-blog". The project includes both the website content and the custom MkDocs theme development.

## Development Commands

### Building and Serving the Site
```bash
# Install dependencies
pip install -r requirements.txt

# Serve the site locally for development
mkdocs serve

# Build the static site
mkdocs build

# Build and serve (combined)
mkdocs serve --dev-addr=0.0.0.0:8000
```

### Theme Development
```bash
# Install the custom theme locally for development
python scripts/install_local.py

# Build the theme package
python -m build

# Install/reinstall theme after changes
pip uninstall mkdocs-simple-blog -y
pip install dist/mkdocs_simple_blog-0.2.0.tar.gz --no-cache-dir
```

## Architecture

### Project Structure
- `docs/` - Website content in Markdown format
  - `index.md` - Homepage content
  - `knowledge-base/` - Technical articles and documentation
  - `IT/` - IT-related content including Kubernetes homelab documentation
  - `assets/` - Static assets (favicon, logo, custom JS)
- `mkdocs_simple_blog/` - Custom MkDocs theme
  - `assets/` - Theme CSS, JS, and images
  - `modules/` - HTML template components
  - `base.html`, `main.html` - Main theme templates
- `site/` - Generated static website output
- `template/` - Theme development files
- `scripts/` - Build and deployment scripts

### Theme Architecture
The custom theme follows MkDocs theme conventions:
- Theme entry point defined in `setup.py` as `simple-blog = mkdocs_simple_blog`
- Modular template system with separate components in `modules/`
- Bootstrap-based responsive design with custom styling
- Configurable components (sidebar, menu, preview, footer)

### Configuration
- `mkdocs.yml` - Main site configuration with theme settings
- `_pyproject.toml` - Python package configuration for theme
- `requirements.txt` - Production dependencies
- Theme supports customization via mkdocs.yml theme section

## Content Management
- All content is in Markdown format in the `docs/` directory
- Navigation structure defined in `mkdocs.yml` nav section
- Custom JavaScript in `docs/assets/custom.js`
- Multilingual content (Italian primary language)

## Theme Customization
The simple-blog theme supports:
- Light/dark theme styles
- Configurable sidebar and navigation
- Custom colors and typography
- Modular components that can be enabled/disabled
- Syntax highlighting with highlight.js