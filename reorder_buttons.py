import os
import re

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}') or '-to-' not in d:
        continue
    
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find the three buttons
    reverse_match = re.search(r'(<a href="/route/[^"]+/" class="cta"[^>]*>.*?Reverse</a>)', html)
    ev_match = re.search(r'(<a href="/ev/[^"]+/" class="ev-link"[^>]*>.*?EV Trip</a>)', html)
    maps_match = re.search(r'(<a href="https://www\.google\.com/maps[^"]*" target="_blank" class="cta maps-btn"[^>]*>.*?Google Maps</a>)', html)
    
    if not (reverse_match and ev_match and maps_match):
        continue
    
    reverse_btn = reverse_match.group(1)
    ev_btn = ev_match.group(1)
    maps_btn = maps_match.group(1)
    
    # Remove all three buttons
    html = html.replace(reverse_btn + '\n            ', '')
    html = html.replace(ev_btn + '\n            ', '')
    html = html.replace(maps_btn, '')
    
    # Find where to insert (after stats div closes)
    # Insert in new order: Maps, Reverse, EV
    new_buttons = f'''            {maps_btn}
            {reverse_btn}
            {ev_btn}'''
    
    # Insert after </div> that closes stats
    html = re.sub(
        r'(</div></div></div>\s*</div>)(\s*</div>\s*<div class="grid">)',
        r'\1\n' + new_buttons + r'\2',
        html
    )
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Reordered buttons on {count} UK route pages")
