# Fllume Documentation

This directory contains the documentation for the Fllume project, including both the landing page website and the Sphinx-generated API documentation.

## Project Structure

```
docs/
├── README.md              # This file
├── Makefile              # Build automation
├── .nojekyll             # Prevents Jekyll processing on GitHub Pages
├── source/               # Sphinx documentation source
│   ├── conf.py          # Sphinx configuration
│   ├── index.rst        # Main documentation index
│   ├── api.rst          # API reference
│   ├── getting-started.rst
│   ├── examples.rst
│   └── _static/         # Static assets (CSS, images, etc.)
├── website/              # Landing page source
│   ├── index.html       # Main landing page
│   ├── css/            # Landing page styles
│   └── js/             # Landing page scripts
└── build/               # Generated documentation (created during build)
    └── html/           # Built Sphinx documentation
```

## Building Documentation Locally

### Prerequisites

1. Install Python dependencies:
   ```bash
   # From the root of the project
   uv pip install -e ".[dev,doc]"
   ```

### Build Commands

From the `docs/` directory, you can use the following make targets:

#### Build HTML Documentation
```bash
make html
```
This builds the Sphinx documentation to `build/html/`.

#### Clean Build Artifacts
```bash
make clean
```
This removes all files from the `build/` directory.

#### Live Development Server
```bash
make livehtml
```
This starts a development server with auto-reload functionality:
- Watches for changes in the `source/` directory
- Automatically rebuilds and refreshes the browser
- Serves on `http://localhost:8000`
- Opens browser automatically

### Manual Build Process

If you prefer not to use the Makefile:

```bash
# It is recommended to run these commands from within the project's virtual
# environment. You can use `uv run` to execute them without activating it.

# Build Sphinx docs from the project root
uv run sphinx-build -b html docs/source docs/build/html

# For live development
uv run sphinx-autobuild docs/source docs/build/html --host 0.0.0.0 --port 8000 --open-browser
```

## GitHub Pages Deployment

The documentation is automatically deployed to GitHub Pages using GitHub Actions.

### How It Works

1. **Trigger**: The deployment runs on:
   - Pushes to the `main` branch
   - Manual workflow dispatch from the Actions tab

2. **Build Process**:
   - Sets up Python 3.11 environment
   - Installs doc dependencies from `pyproject.toml`
   - Builds the Sphinx documentation
   - Assembles a final site with the landing page at the root and the
     Sphinx documentation in a `/docs/` subdirectory.
   - Deploys to GitHub Pages

3. **Site Structure**:
   - **Root (`/`)**: Landing page from `docs/website/`
   - **Documentation (`/docs/`)**: Sphinx-generated docs

### Workflow File

The deployment is configured in `.github/workflows/deploy-docs.yml` with:
- Proper permissions for GitHub Pages
- Concurrency control to prevent conflicts
- Two-job setup (build + deploy) for security

### Manual Deployment

You can manually trigger deployment from the GitHub Actions tab:
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Select "Deploy Documentation to GitHub Pages"
4. Click "Run workflow"

## Local Development Workflow

For the best development experience:

1. **Start the live server**:
   ```bash
   cd docs
   make livehtml
   ```

2. **Edit documentation**:
   - Modify files in `docs/source/`
   - Changes are automatically detected and rebuilt
   - Browser refreshes automatically

3. **Test landing page**:
   - Edit files in `docs/website/`
   - Open `docs/website/index.html` directly in browser
   - Or serve with a simple HTTP server

## Important Configuration Notes

### Sphinx Configuration
- Configuration is in `docs/source/conf.py`
- Custom CSS is in `docs/source/_static/custom.css`
- Extensions and theme settings are configured for optimal GitHub Pages compatibility

### GitHub Pages Settings
- **Source**: GitHub Actions (not branch-based)
- **Custom Domain**: Configure in repository settings if needed
- **HTTPS**: Automatically enabled by GitHub Pages

### Dependencies
- All documentation dependencies are managed in `pyproject.toml` under the `doc` optional-dependency group.

### Troubleshooting

**Build fails locally**:
- Check that all dependencies are installed from the project root: `uv pip install -e ".[doc]"`
- Ensure you're in the `docs/` directory when running make commands

**GitHub Pages deployment fails**:
 Check the Actions tab for detailed error logs
- Ensure repository has Pages enabled in Settings

**Live reload not working**:
- Make sure `sphinx-autobuild` is installed
- Check that port 8000 is not in use by another process
- Try manually specifying a different port: `sphinx-autobuild source build/html --port 8001`