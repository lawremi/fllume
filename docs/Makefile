# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=

# Point to the executables in the project's virtual environment
# This ensures that the correct dependencies are found.
VENV_PATH       ?= ../.venv
SPHINXBUILD     ?= $(VENV_PATH)/bin/sphinx-build
SPHINXAUTOBUILD ?= $(VENV_PATH)/bin/sphinx-autobuild
SOURCEDIR    = source
BUILDDIR     = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Build HTML documentation
html:
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O)
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

# Clean build artifacts
clean:
	@rm -rf $(BUILDDIR)/*
	@echo "Build directory cleaned."

# Live HTML with auto-reload for development
livehtml:
	@echo "Starting live HTML server with auto-reload..."
	@$(SPHINXAUTOBUILD) "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS) $(O) \
		--host 0.0.0.0 \
		--port 8000 \
		--open-browser \
		--watch "$(SOURCEDIR)" \
		--ignore "*.tmp" \
		--ignore "*.swp" \
		--ignore "*~"

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)