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
    
    maps_btn = f'<a href="https://www.google.com/maps/dir/{from_city}/{to_city}" target="_blank" class="cta maps-btn"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg> Open in Google Maps</a>'
    
    # Add CSS for maps-btn
    if '.maps-btn' not in html:
        html = html.replace('.cta {', '.maps-btn { background: #EFA24F; color: white; margin-left: 0.5rem; }\n        .cta {')
    
    # Try different patterns
    if 'class="ev-link"' in html:
        html = re.sub(
            r'(<a href="/ev/[^"]+/"[^>]*class="[^"]*ev-link[^"]*"[^>]*>[^<]*</a>)',
            r'\1\n            ' + maps_btn,
            html
        )
    elif 'class="cta reverse-btn"' in html:
        html = re.sub(
            r'(<a href="/route/[^"]+/"[^>]*>[^<]*</a>)\s*</div>\s*</div>\s*</section>',
            r'\1\n            ' + maps_btn + r'\n        </div>\n        </div>\n    </section>',
            html
        )
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added Google Maps link to {count} UK route pages")
