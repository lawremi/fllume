// Main JavaScript functionality for fllume website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initTabs();
    initCopyButtons();
    initSmoothScrolling();
    initNavHighlight();
});

/**
 * Initialize tab functionality for installation section
 */
function initTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button and corresponding pane
            this.classList.add('active');
            document.getElementById(targetTab).classList.add('active');
        });
    });
}

/**
 * Initialize copy button functionality
 */
function initCopyButtons() {
    const copyButtons = document.querySelectorAll('.copy-btn');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            let textToCopy = '';
            
            // Check if button has data-copy attribute (for simple text)
            if (this.hasAttribute('data-copy')) {
                textToCopy = this.getAttribute('data-copy');
            }
            // Check if button has data-copy-code attribute (for code blocks)
            else if (this.hasAttribute('data-copy-code')) {
                const codeBlock = this.parentElement.querySelector('code');
                textToCopy = codeBlock ? codeBlock.textContent : '';
            }
            // Fallback: get text from sibling code element
            else {
                const codeBlock = this.parentElement.querySelector('code');
                textToCopy = codeBlock ? codeBlock.textContent : '';
            }
            
            // Copy to clipboard
            copyToClipboard(textToCopy, this);
        });
    });
}

/**
 * Copy text to clipboard and show feedback
 */
function copyToClipboard(text, button) {
    // Use modern clipboard API if available
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyFeedback(button);
        }).catch(err => {
            console.error('Failed to copy text: ', err);
            fallbackCopyToClipboard(text, button);
        });
    } else {
        // Fallback for older browsers
        fallbackCopyToClipboard(text, button);
    }
}

/**
 * Fallback copy method for older browsers
 */
function fallbackCopyToClipboard(text, button) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    try {
        document.execCommand('copy');
        showCopyFeedback(button);
    } catch (err) {
        console.error('Fallback: Failed to copy text: ', err);
    }
    
    document.body.removeChild(textArea);
}

/**
 * Show visual feedback when text is copied
 */
function showCopyFeedback(button) {
    const originalText = button.textContent;
    button.textContent = 'Copied!';
    button.classList.add('copied');
    
    setTimeout(() => {
        button.textContent = originalText;
        button.classList.remove('copied');
    }, 2000);
}

/**
 * Initialize smooth scrolling for navigation links
 */
function initSmoothScrolling() {
    const navLinks = document.querySelectorAll('a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Initialize navigation highlight on scroll
 */
function initNavHighlight() {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link[href^="#"]');
    
    if (sections.length === 0 || navLinks.length === 0) return;
    
    function highlightNavigation() {
        const scrollPosition = window.scrollY + 100;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }
    
    // Throttle scroll events for better performance
    let ticking = false;
    function onScroll() {
        if (!ticking) {
            requestAnimationFrame(() => {
                highlightNavigation();
                ticking = false;
            });
            ticking = true;
        }
    }
    
    window.addEventListener('scroll', onScroll);
    
    // Initial highlight
    highlightNavigation();
}

/**
 * Utility function to debounce function calls
 */
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction() {
        const context = this;
        const args = arguments;
        
        const later = function() {
            timeout = null;
            if (!immediate) func.apply(context, args);
        };
        
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        
        if (callNow) func.apply(context, args);
    };
}

/**
 * Add loading states and error handling for external resources
 */
function handleExternalResources() {
    // Check if Prism.js loaded successfully
    if (typeof Prism === 'undefined') {
        console.warn('Prism.js failed to load. Syntax highlighting may not work.');
    }
    
    // Check if Google Fonts loaded
    const testElement = document.createElement('div');
    testElement.style.fontFamily = 'Inter, sans-serif';
    testElement.style.position = 'absolute';
    testElement.style.visibility = 'hidden';
    testElement.textContent = 'Test';
    document.body.appendChild(testElement);
    
    const computedFont = window.getComputedStyle(testElement).fontFamily;
    if (!computedFont.includes('Inter')) {
        console.warn('Inter font failed to load. Falling back to system fonts.');
    }
    
    document.body.removeChild(testElement);
}

// Handle external resources after DOM is loaded
document.addEventListener('DOMContentLoaded', handleExternalResources);

// Add keyboard navigation support
document.addEventListener('keydown', function(e) {
    // Handle tab navigation for copy buttons
    if (e.key === 'Enter' || e.key === ' ') {
        if (e.target.classList.contains('copy-btn')) {
            e.preventDefault();
            e.target.click();
        }
        if (e.target.classList.contains('tab-button')) {
            e.preventDefault();
            e.target.click();
        }
    }
});

// Add focus management for accessibility
document.addEventListener('DOMContentLoaded', function() {
    // Add focus indicators for keyboard navigation
    const focusableElements = document.querySelectorAll(
        'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );
    
    focusableElements.forEach(element => {
        element.addEventListener('focus', function() {
            this.classList.add('keyboard-focus');
        });
        
        element.addEventListener('blur', function() {
            this.classList.remove('keyboard-focus');
        });
        
        element.addEventListener('mousedown', function() {
            this.classList.remove('keyboard-focus');
        });
    });
});

// Performance optimization: Lazy load non-critical features
function initLazyFeatures() {
    // Add intersection observer for animations
    if ('IntersectionObserver' in window) {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);
        
        // Observe elements that should animate in
        const animateElements = document.querySelectorAll('.feature, .doc-card');
        animateElements.forEach(el => observer.observe(el));
    }
}

// Initialize lazy features after a short delay
setTimeout(initLazyFeatures, 100);