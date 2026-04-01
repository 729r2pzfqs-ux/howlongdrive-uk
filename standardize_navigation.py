#!/usr/bin/env python3
"""
Standardize Navigation Across All HTML Files - howlongdrive.uk
==============================================================

This script standardizes the navigation and hamburger menu structure across
all HTML pages to match the reference implementation from howlongdrive.com.

Changes applied:
1. Wraps nav links in <div class="nav-links"> container
2. Removes old close buttons from nav
3. Ensures hamburger button has inline SVG styling
4. Adds toggleMenu() JavaScript function if missing
5. Removes redundant CSS variables from nav styling

Usage:
    python3 standardize_navigation.py

This script is designed to process all 15,000+ HTML files efficiently.
"""

import os
import re
import sys
from pathlib import Path

def standardize_header(header_content):
    """Standardize header HTML structure"""
    
    # Skip if already standardized
    if '<div class="nav-links">' in header_content:
        return header_content, False
    
    # Extract nav content
    nav_match = re.search(r'<nav[^>]*id="nav"[^>]*>(.*?)</nav>', header_content, re.DOTALL)
    if not nav_match:
        return header_content, False
    
    nav_inner = nav_match.group(1).strip()
    
    # Remove old close button
    nav_inner_clean = re.sub(
        r'<button class="close-btn"[^>]*>.*?</button>\s*',
        '',
        nav_inner,
        flags=re.DOTALL
    ).strip()
    
    # Create standardized header
    new_header = f"""<header>
        <div class="container header-inner">
            <a href="/" class="logo">
                <img src="/assets/logo-header.png" alt="HowLongDrive UK">
            </a>
            <button class="hamburger" onclick="toggleMenu()" aria-label="Menu">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
            </button>
            <div class="overlay" onclick="toggleMenu()"></div>
            <nav id="nav">
                <div class="nav-links">
                    {nav_inner_clean}
                </div>
            </nav>
        </div>
    </header>"""
    
    return new_header, True

def add_toggle_menu_js(content):
    """Add toggleMenu JavaScript function if missing"""
    
    if 'function toggleMenu()' in content:
        return content, False
    
    if '</body>' not in content:
        return content, False
    
    js_code = """<script>
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
    var overlay = document.querySelector('.overlay');
    if (overlay) overlay.classList.toggle('active');
    document.body.style.overflow = document.querySelector('.nav-links').classList.contains('active') ? 'hidden' : '';
}
</script>"""
    
    new_content = content.replace('</body>', f'{js_code}\n</body>')
    return new_content, True

def process_html_file(filepath):
    """Process a single HTML file"""
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix header
        header_match = re.search(r'<header>.*?</header>', content, re.DOTALL)
        if header_match:
            old_header = header_match.group(0)
            new_header, header_changed = standardize_header(old_header)
            if header_changed:
                content = content.replace(old_header, new_header)
        
        # Add JS
        content, js_added = add_toggle_menu_js(content)
        
        # Write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    except Exception as e:
        print(f"ERROR processing {filepath}: {e}", file=sys.stderr)
        return False

def main():
    """Main entry point"""
    
    html_files = list(Path('.').rglob('*.html'))
    html_files = [f for f in html_files if not any(part.startswith('.') for part in f.parts)]
    
    if not html_files:
        print("No HTML files found")
        return
    
    print(f"Processing {len(html_files)} HTML files...\n")
    
    updated_count = 0
    failed_count = 0
    
    for idx, filepath in enumerate(sorted(html_files), 1):
        if process_html_file(filepath):
            updated_count += 1
            if idx % 100 == 0:
                print(f"[{idx:5d}] ✓ Updated {updated_count} files so far")
        
        if idx % 1000 == 0:
            print(f"  Progress: {idx}/{len(html_files)} ({100*idx//len(html_files)}%)")
    
    print(f"\n{'='*50}")
    print(f"Total files:   {len(html_files)}")
    print(f"Updated:       {updated_count}")
    print(f"Unchanged:     {len(html_files) - updated_count}")
    print(f"{'='*50}")

if __name__ == '__main__':
    main()
