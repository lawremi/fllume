# fllume Website Plan

## Project Overview

fllume is a fluent Python API for data scientists to build and interact with Large Language Model (LLM) agents. The website should effectively communicate its value proposition, showcase its simplicity, and guide users to get started quickly.

## Website Goals

1. **Communicate Value**: Clearly explain what fllume is and why data scientists should use it
2. **Showcase Simplicity**: Demonstrate the fluent API's ease of use
3. **Quick Start**: Help users get up and running quickly
4. **Examples**: Show practical use cases with code examples
5. **Documentation**: Provide comprehensive API documentation via Sphinx

## Technology Stack

### Landing Page (Simple & Maintainable)
- **HTML5**: Semantic markup for content structure
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: For interactive elements (syntax highlighting, copy buttons)
- **Prism.js**: Lightweight syntax highlighting for code examples
- **Inter Font**: Clean, modern typography (via Google Fonts)

### Documentation (Auto-generated)
- **Sphinx**: Documentation generator for Python projects
- **Napoleon**: Sphinx extension for Google/NumPy style docstrings
- **sphinx-rtd-theme**: Read the Docs theme for consistent documentation styling
- **sphinx-autodoc**: Automatic API documentation from docstrings
- **MyST**: Markdown support for Sphinx (optional, for markdown docs)

## File Structure

```
docs/                       # Documentation root
├── website/               # Landing page files
│   ├── index.html         # Main homepage
│   ├── css/
│   │   ├── style.css      # Main stylesheet
│   │   └── prism-tomorrow.css # Code syntax highlighting
│   ├── js/
│   │   ├── main.js        # Main JavaScript functionality
│   │   └── prism.js       # Syntax highlighting library
│   ├── assets/
│   │   ├── favicon.ico    # Website favicon
│   │   └── og-image.png   # Open Graph image
│   └── CNAME              # GitHub Pages custom domain
│
├── source/                # Sphinx documentation source
│   ├── conf.py            # Sphinx configuration
│   ├── index.rst          # Documentation homepage
│   ├── installation.rst   # Installation guide
│   ├── quickstart.rst     # Quick start guide
│   ├── api/               # API documentation
│   │   ├── agent.rst      # Agent class documentation
│   │   └── builder.rst    # AgentBuilder documentation
│   ├── examples/          # Example notebooks/scripts
│   │   ├── data_standardization.rst
│   │   ├── tool_integration.rst
│   │   └── streaming.rst
│   └── _static/           # Static assets for Sphinx
│       └── custom.css     # Custom styling
│
├── build/                 # Sphinx build output (gitignored)
│   └── html/              # Generated HTML documentation
│
├── Makefile               # Sphinx build commands
└── requirements-docs.txt  # Documentation dependencies
```

## Website Architecture

### 1. Landing Page (`/`)
Single-page marketing site hosted at root with sections for:
- Hero/Introduction
- Features
- Installation
- Quick examples
- Links to full documentation

### 2. Documentation (`/docs/` or subdomain)
Comprehensive Sphinx-generated documentation including:
- Getting Started Guide
- API Reference (auto-generated from docstrings)
- Detailed Examples
- Advanced Usage
- Contributing Guide

## Landing Page Structure

### 1. Header/Navigation
- Logo/Project name "fllume"
- Navigation links: Home, Documentation, API Reference, GitHub
- Clean, minimal design with sticky behavior

### 2. Hero Section
- **Tagline**: "A Fluent Python API for LLM Agents"
- **Subtitle**: "Simplify LLM interactions for data science workflows"
- **CTA Buttons**: 
  - "Get Started" (links to documentation)
  - "View on GitHub" (external link)
- **Code Preview**: Simple example showing the fluent API in action

### 3. Features Section
Three column layout highlighting key benefits:

#### Column 1: Fluent API
- **Icon**: Code/brackets icon
- **Title**: "Pythonic & Fluent"
- **Description**: "Chain methods naturally with a readable, intuitive API designed for data scientists"

#### Column 2: Tool Integration
- **Icon**: Tool/wrench icon
- **Title**: "Easy Tool Integration"
- **Description**: "Convert Python functions into LLM tools with automatic schema generation"

#### Column 3: Structured Output
- **Icon**: Schema/structure icon
- **Title**: "Structured Responses"
- **Description**: "Get consistent, typed responses using Pydantic models"

### 4. Installation Section
- **Title**: "Get Started in Seconds"
- **Two tabs**: "Using uv" (default) and "Using pip"
- **Copy buttons** for each command
- **Link**: "Full installation guide →" (to Sphinx docs)

### 5. Quick Example Section
- **Title**: "See It In Action"
- **One compelling example** with syntax highlighting
- **Link**: "More examples →" (to Sphinx docs)

### 6. Documentation CTA Section
- **Title**: "Ready to Dive Deeper?"
- **Cards** linking to:
  - Getting Started Guide
  - API Reference
  - Examples Gallery
  - GitHub Repository

### 7. Footer
- **Links**: Documentation, GitHub, Issues, PyPI
- **Copyright**: MIT License notice
- **Author**: Credit to Michael Lawrence

## Sphinx Documentation Structure

### 1. Configuration (`conf.py`)
```python
# Key configurations
project = 'fllume'
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_rtd_theme',
    'myst_parser',  # Optional: for markdown support
]
html_theme = 'sphinx_rtd_theme'
napoleon_google_docstring = True
autodoc_typehints = 'description'
```

### 2. Documentation Pages

#### Home (`index.rst`)
- Welcome message
- What is fllume?
- Key features
- Quick links to guides

#### Installation (`installation.rst`)
- Requirements
- Installation methods (uv, pip, development)
- Environment setup
- Troubleshooting

#### Quick Start (`quickstart.rst`)
- First agent
- Basic examples
- Common patterns

#### API Reference (`api/`)
- Auto-generated from docstrings
- `Agent` class documentation
- `AgentBuilder` class documentation
- Type definitions
- Exceptions

#### Examples (`examples/`)
- Detailed walkthroughs
- Complete code samples
- Use case scenarios
- Best practices

## Design Principles

### Visual Design
1. **Consistency**: Landing page and Sphinx docs should feel cohesive
2. **Color Scheme**:
   - Primary: Deep blue (#1e3a8a)
   - Accent: Bright blue (#3b82f6)
   - Background: Light gray (#f9fafb)
   - Code blocks: Dark theme for contrast
3. **Typography**:
   - Headers: Inter (bold weights)
   - Body: Inter (regular)
   - Code: JetBrains Mono or similar monospace

### Documentation Best Practices
1. **Comprehensive Docstrings**: Every public method/class documented
2. **Type Hints**: Full type annotations for better documentation
3. **Examples in Docstrings**: Show usage directly in API docs
4. **Cross-references**: Link between related concepts
5. **Search**: Sphinx built-in search functionality

## Implementation Plan

### Phase 1: Documentation Setup
1. Set up Sphinx configuration
2. Write comprehensive docstrings (if not already present)
3. Create documentation structure
4. Write guides and examples
5. Configure GitHub Actions for auto-building docs

### Phase 2: Landing Page
1. Create HTML/CSS/JS structure
2. Implement responsive design
3. Add interactive elements
4. Optimize for performance
5. Deploy to GitHub Pages

### Phase 3: Integration
1. Link landing page to documentation
2. Ensure consistent styling
3. Set up custom domain (if desired)
4. Configure deployment pipeline

## Deployment Strategy

### GitHub Pages Setup
```
github.com/lawremi/fllume/
├── index.html (redirects to website/)
├── website/ (landing page)
└── docs/ (Sphinx output)
```

### Build Process
1. **Documentation**: GitHub Actions builds Sphinx on push
2. **Landing Page**: Static files, no build needed
3. **Deployment**: Both pushed to `gh-pages` branch

## Future Enhancements

### Phase 2 Features
- Interactive playground
- Video tutorials
- Blog/changelog section
- Community examples
- LLM provider comparison

### Documentation Enhancements
- Jupyter notebook integration
- API versioning
- Multi-language examples
- Performance benchmarks
- Migration guides

## Success Metrics
- Documentation completeness (100% public API documented)
- Time to first successful API call
- Documentation search effectiveness
- Page load speed < 2 seconds
- SEO ranking for "Python LLM agent"

## Conclusion

This hybrid approach provides the best of both worlds: an attractive, fast-loading landing page for marketing and discovery, paired with comprehensive Sphinx-generated documentation for detailed API reference and guides. The use of Napoleon ensures that the existing Google-style docstrings in the codebase will be properly rendered in the documentation.