import os
import re

count = 0

for d in os.listdir('route'):
    if not os.path.isdir(f'route/{d}') or '-to-' not in d:
        continue
    
    path = f'route/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    # Find the buttons section (after stats, before </div></div>)
    # Match the three buttons in current order
    pattern = r'''(<a href="/route/[^"]+/" class="cta"[^>]*>.*?Reverse</a>)\s*
            (<a href="/ev/[^"]+/" class="ev-link"[^>]*>.*?EV Trip</a>)\s*
            (<a href="https://www\.google\.com/maps[^"]+?" target="_blank" class="cta maps-btn"[^>]*>.*?Google Maps</a>)'''
    
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        continue
    
    reverse_btn = match.group(1)
    ev_btn = match.group(2)
    maps_btn = match.group(3)
    
    # New order: Maps, Reverse, EV
    new_order = f'''{maps_btn}
            {reverse_btn}
            {ev_btn}'''
    
    html = html[:match.start()] + new_order + html[match.end():]
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Reordered buttons on {count} UK route pages")
