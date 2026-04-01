#!/usr/bin/env python3
"""
Standardize navigation and hamburger menu across all HTML pages in howlongdrive-uk.
This script:
1. Wraps all nav links in a <div class="nav-links"> wrapper
2. Ensures the SVG hamburger icon has proper styling
3. Ensures the toggleMenu() JavaScript function exists
4. Removes old close buttons from the nav
"""

import os
import re

def process_html_file(filepath):
    """Process a single HTML file to standardize navigation"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = 0
    
    # Fix 1: Add nav-links wrapper if missing
    header_match = re.search(r'<header>.*?</header>', content, re.DOTALL)
    if header_match:
        old_header = header_match.group(0)
        
        if '<div class="nav-links">' not in old_header:
            nav_match = re.search(r'<nav[^>]*id="nav"[^>]*>(.*?)</nav>', old_header, re.DOTALL)
            if nav_match:
                nav_inner = nav_match.group(1).strip()
                
                # Remove old close button
                nav_inner = re.sub(r'<button class="close-btn"[^>]*>.*?</button>\s*', '', nav_inner, flags=re.DOTALL).strip()
                
                # Create new header with nav-links wrapper
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
                    {nav_inner}
                </div>
            </nav>
        </div>
    </header>"""
                
                content = content.replace(old_header, new_header)
                changes += 1
    
    # Fix 2: Ensure toggleMenu() function exists
    if 'function toggleMenu()' not in content and '</body>' in content:
        js_code = """<script>
function toggleMenu() {
    document.querySelector('.nav-links').classList.toggle('active');
    var overlay = document.querySelector('.overlay');
    if (overlay) overlay.classList.toggle('active');
    document.body.style.overflow = document.querySelector('.nav-links').classList.contains('active') ? 'hidden' : '';
}
</script>"""
        content = content.replace('</body>', f'{js_code}\n</body>')
        changes += 1
    
    if changes > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    
    return False

def main():
    """Process all HTML files in the repository"""
    updated_count = 0
    total_count = 0
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and node_modules
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                total_count += 1
                
                try:
                    if process_html_file(filepath):
                        updated_count += 1
                        print(f"✓ Updated: {filepath}")
                except Exception as e:
                    print(f"✗ Error processing {filepath}: {e}")
    
    print(f"\nSummary:")
    print(f"  Total HTML files: {total_count}")
    print(f"  Updated: {updated_count}")

if __name__ == '__main__':
    main()
