# Visual Layer SDK Documentation

This directory contains the documentation for the Visual Layer SDK, built with Sphinx and the Furo theme.

## Documentation Structure

- `index.rst` - Homepage and overview (main entry point)
- `installation.md` - Installation instructions
- `getting-started.md` - Basic usage guide
- `api-reference.md` - Complete API documentation
- `search-filtering.md` - Advanced search capabilities
- `logging.md` - Logging system documentation

## Local Development

To build and run the documentation locally:

1. **Install Python Dependencies**
   ```bash
   cd docs
   pip install -r requirements.txt
   ```

2. **Build Documentation**
   ```bash
   # Build HTML documentation
   make html
   
   # Or use the live reload server for development
   make livehtml
   ```

3. **View Documentation**
   Open `_build/html/index.html` in your browser, or if using live reload, go to http://localhost:8000

## Available Make Commands

- `make html` - Build HTML documentation
- `make livehtml` - Start live reload server for development
- `make clean` - Clean build directory
- `make linkcheck` - Check for broken links

## Deployment

The documentation is automatically deployed using GitHub Actions when changes are pushed to the main branch. The workflow builds the Sphinx documentation and deploys it to GitHub Pages.

## Sphinx Configuration

- **Configuration**: `conf.py` - Main Sphinx configuration
- **Theme**: Furo - Modern, responsive documentation theme
- **Extensions**: 
  - `myst_parser` - Markdown support
  - `sphinx.ext.autodoc` - Auto-generate API docs
  - `sphinx.ext.napoleon` - Google/NumPy style docstrings
  - `sphinx_copybutton` - Copy button for code blocks

## Content Guidelines

### Code Examples

Use syntax highlighting for code blocks:

```python
from visual_layer_sdk import VisualLayerClient

client = VisualLayerClient(api_key="key", api_secret="secret")
```

### Links

- Use relative links for internal pages: `[Getting Started](getting-started.md)`
- MyST parser will handle cross-references automatically
- External links use standard markdown syntax

### Formatting

- Use emojis to make content more engaging
- Include code examples for all features
- Add troubleshooting sections where relevant
- Use consistent heading structure (H1 for page title, H2 for sections, etc.)

## Adding New Pages

1. Create a new `.md` or `.rst` file in the `docs/` directory
2. Add the page to the toctree in `index.rst`:
   ```rst
   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      installation
      getting-started
      your-new-page
   ```

## Maintenance

### Updating Documentation

1. Edit the relevant `.md` or `.rst` files
2. Test changes locally with `make html` or `make livehtml`
3. Commit and push changes to trigger automatic deployment
4. Verify the live site updates correctly

### Adding New SDK Features

When adding new SDK features:

1. Update the relevant documentation pages
3. Update the API reference in `api-reference.md`
4. Include logging information if applicable
5. Test all examples to ensure they work

## Troubleshooting

### Common Issues

**Build fails:**
- Check Python dependencies: `pip install -r requirements.txt`
- Verify all markdown files have proper syntax
- Check for broken cross-references

**Pages not updating:**
- Check GitHub Actions workflow status
- Verify the build completes successfully
- Look for build errors in the Actions tab

**Styling not applied:**
- Verify Furo theme is installed: `pip show furo`
- Check `conf.py` configuration
- Clear browser cache

**Navigation not working:**
- Check that all pages are included in the toctree in `index.rst`
- Verify file names match toctree entries
- Ensure proper indentation in RST files

For more help, see the [Sphinx documentation](https://www.sphinx-doc.org/) or [Furo theme documentation](https://pradyunsg.me/furo/).