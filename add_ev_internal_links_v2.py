import os
import re
from collections import defaultdict

# Build route map
route_map = defaultdict(list)
for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}') or '-to-' not in d:
        continue
    parts = d.split('-to-')
    from_city = parts[0]
    to_city = parts[1]
    route_map[from_city].append(to_city)
    route_map[to_city].append(from_city)

count = 0

for d in os.listdir('ev'):
    if not os.path.isdir(f'ev/{d}') or '-to-' not in d:
        continue
    
    parts = d.split('-to-')
    from_slug = parts[0]
    to_slug = parts[1]
    from_city = from_slug.replace('-', ' ').title()
    to_city = to_slug.replace('-', ' ').title()
    
    path = f'ev/{d}/index.html'
    
    with open(path) as f:
        html = f.read()
    
    if 'More EV routes from' in html:
        continue
    
    from_routes = route_map.get(from_slug, [])[:4]
    to_routes = route_map.get(to_slug, [])[:4]
    
    links_html = '    <div class="related-section">'
    
    if from_routes:
        links_html += f'<div class="related-group"><h4>More EV routes from {from_city}</h4><div class="related-links">'
        for dest in from_routes[:3]:
            if dest != to_slug:
                dest_name = dest.replace('-', ' ').title()
                links_html += f'<a href="/ev/{from_slug}-to-{dest}/">{dest_name}</a>'
        links_html += '</div></div>'
    
    if to_routes:
        links_html += f'<div class="related-group"><h4>EV routes to {to_city}</h4><div class="related-links">'
        for orig in to_routes[:3]:
            if orig != from_slug:
                orig_name = orig.replace('-', ' ').title()
                links_html += f'<a href="/ev/{orig}-to-{to_slug}/">From {orig_name}</a>'
        links_html += '</div></div>'
    
    links_html += f'<div class="related-group"><h4>Petrol Route</h4><div class="related-links"><a href="/route/{from_slug}-to-{to_slug}/">View petrol route: {from_city} to {to_city}</a></div></div>'
    links_html += '</div>\n'
    
    # Insert before footer
    html = html.replace('    <footer>', links_html + '    <footer>')
    
    with open(path, 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Added internal links to {count} UK EV pages")
