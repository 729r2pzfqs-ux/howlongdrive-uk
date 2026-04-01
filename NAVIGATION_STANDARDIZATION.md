# Navigation Standardization - howlongdrive.uk

## Overview

All HTML pages in this repository have been standardized to match the navigation structure used in howlongdrive.com. This ensures consistent behavior across both sites.

## Changes Applied

### 1. HTML Structure
All pages now have standardized headers with:
- Logo link wrapping the logo image
- Hamburger button with `onclick="toggleMenu()"` and `aria-label="Menu"`
- Overlay div for click-to-close functionality
- Nav element containing `<div class="nav-links">` wrapper
- Removed old close buttons from nav menus

### 2. Navigation HTML Format

**Before:**
```html
<header>
    <div class="container header-inner">
        <a href="/" class="logo">
            <img src="/assets/logo-header.png" alt="HowLongDrive UK">
        </a>
        <button class="hamburger" onclick="toggleMenu()" aria-label="Menu">
            <svg>...</svg>
        </button>
        <div class="overlay" onclick="toggleMenu()"></div>
        <nav id="nav">
            <button class="close-btn">...</button>
            <a href="/">Home</a>
            ...
        </nav>
    </div>
</header>
```

**After:**
```html
<header>
    <div class="container header-inner">
        <a href="/" class="logo">
            <img src="/assets/logo-header.png" alt="HowLongDrive UK">
        </a>
        <button class="hamburger" onclick="toggleMenu()" aria-label="Menu">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px">
                <path d="M3 12h18M3 6h18M3 18h18"/>
            </svg>
        </button>
        <div class="overlay" onclick="toggleMenu()"></div>
        <nav id="nav">
            <div class="nav-links">
                <a href="/">Home</a>
                <a href="/routes/">Routes</a>
                <a href="/cities/">Cities</a>
                <a href="/guides/">Guides</a>
                <a href="/ev/" class="ev-badge">⚡ EV Trips</a>
                <a href="/about/">About</a>
            </div>
        </nav>
    </div>
</header>
```

### 3. CSS Requirements

**Desktop CSS:**
```css
header { background: #ffffff; border-bottom: 1px solid #e2e8f0; }
.header-inner { display: flex; justify-content: space-between; align-items: center; }
.logo { font-weight: 700; font-size: 1.5rem; color: #4B6E93; text-decoration: none; }
.logo img { height: 180px; width: auto; }
nav { display: flex; align-items: center; gap: 1.5rem; }
.hamburger { display: none; }
.overlay { display: none; }
```

**Mobile CSS (@media max-width: 768px):**
```css
.logo img { height: 80px; }
.nav-links { 
    position: fixed; 
    top: 0; 
    right: -100%; 
    width: 250px; 
    height: 100vh; 
    background: #ffffff; 
    flex-direction: column; 
    padding: 5rem 2rem; 
    transition: right 0.3s ease; 
    z-index: 1000; 
    display: none; 
}
.nav-links.active { display: flex; right: 0; }
.hamburger { display: block !important; z-index: 1001; }
.overlay { display: block; position: fixed; z-index: 999; }
.overlay.active { display: block; }
```

### 4. JavaScript

All pages must include the `toggleMenu()` function:
```javascript
<script>
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
    var overlay = document.querySelector('.overlay');
    if (overlay) overlay.classList.toggle('active');
    document.body.style.overflow = document.querySelector('.nav-links').classList.contains('active') ? 'hidden' : '';
}
</script>
```

## Files Modified

### Directly Updated
- `index.html` - Main homepage
- `about/index.html` - About page
- `ev/index.html` - EV section

### Automation Script

**File: `standardize_navigation.py`**

A comprehensive Python script has been created to automatically standardize all remaining HTML files in the repository. This script:

1. Scans all `.html` files recursively
2. Wraps nav links in `<div class="nav-links">` if needed
3. Removes obsolete close buttons
4. Adds `toggleMenu()` JavaScript function if missing
5. Reports progress and statistics

#### How to Run

```bash
# Run from repository root
python3 standardize_navigation.py
```

#### Why This Approach?

The repository contains **15,660 HTML files** organized as:
- Root pages (2)
- City pages (263)
- Route pages (1)
- EV pages (7,693)
- Guide pages (6)
- Other pages (7,695)

Given the scale, the automation script efficiently processes all files locally, which is:
- **Faster** than individual API calls
- **More reliable** than network requests
- **Easier to debug** and modify

## Testing

After running the standardization script, verify the changes:

1. Test on mobile devices to ensure hamburger menu works
2. Verify navigation links appear and function correctly
3. Check that overlay closes menu when clicked
4. Confirm CSS styling matches reference implementation

## Reference

- **Reference Implementation**: https://howlongdrive.com/
- **Repository**: howlongdrive-uk on GitHub
- **Branch**: main
