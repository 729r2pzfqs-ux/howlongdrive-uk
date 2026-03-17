import os
import re

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}'):
        continue
    
    if '-to-' not in d:
        continue
    
    parts = d.split('-to-')
    from_city = parts[0].replace('-', ' ').title()
    to_city = parts[1].replace('-', ' ').title()
    
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    if 'google.com/maps' in html:
        continue
    
    maps_btn = f'<a href="https://www.google.com/maps/dir/{from_city}/{to_city}" target="_blank" class="cta maps-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg> Google Maps</a>'
    
    # Add CSS for maps-btn if not present
    if '.maps-btn' not in html:
        html = html.replace('.ev-link {', '.maps-btn { background: #EFA24F; margin-left: 0.75rem; }\n        .ev-link {')
    
    # Add after ev-link
    html = re.sub(
        r'(class="ev-link"[^>]*>.*?</a>)',
        r'\1\n            ' + maps_btn,
        html
    )
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added Google Maps link to {count} UK route pages")
