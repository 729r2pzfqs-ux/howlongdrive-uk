import json
import os

routes = []
for f in ['data/routes.json', 'data/routes_commute.json', 'data/routes_expansion.json', 'data/routes_bulk.json']:
    if os.path.exists(f):
        with open(f, 'r') as file:
            routes.extend(json.load(file))

with open('data/city_coords.json', 'r') as f:
    coords = json.load(f)


# Build route lookups for Related Routes
from collections import defaultdict
routes_from = defaultdict(list)
routes_to = defaultdict(list)
for r in routes:
    routes_from[r['from']].append(r)
    routes_to[r['to']].append(r)

def format_slug(city):
    return city.lower().replace(' ', '-').replace("'", "")

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>How Long to Drive from {from_city} to {to_city}? {time}, {miles} Miles</title>
    <meta name="description" content="How long to drive from {from_city} to {to_city}? {time} driving time, {miles} miles via {highway}. Get petrol costs, best times to drive, and route details.">
    <link rel="canonical" href="https://howlongdrive.uk/route/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#4B6E93">
    <meta property="og:title" content="{from_city} to {to_city} - {time} Drive Time">
    <meta property="og:description" content="Driving time from {from_city} to {to_city}: {time}, {miles} miles">
    <meta property="og:image" content="https://howlongdrive.uk/assets/og-image.png">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"How long does it take to drive from {from_city} to {to_city}?","acceptedAnswer":{{"@type":"Answer","text":"The drive from {from_city} to {to_city} takes approximately {time} covering {miles} miles via {highway}."}}}},{{"@type":"Question","name":"How much does petrol cost for {from_city} to {to_city}?","acceptedAnswer":{{"@type":"Answer","text":"At 40 MPG and £1.40/litre, expect to spend approximately £{petrol_cost} on petrol for this {miles}-mile trip."}}}},{{"@type":"Question","name":"What is the best time to drive from {from_city} to {to_city}?","acceptedAnswer":{{"@type":"Answer","text":"{best_time} to avoid heavy traffic."}}}}]}}</script>
    <style>
        :root {{ --primary: #4B6E93; --primary-dark: #3a5775; --accent: #EFA24F; --green: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 700; font-size: 1.5rem; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.75rem; }}
        .logo img {{ height: 180px; width: auto; }}
        nav {{ display: flex; align-items: center; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        nav a:hover {{ color: var(--primary); }}
        .ev-badge {{ background: var(--green); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }}
        .close-btn {{ display: none; }} .hamburger {{ display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; }}
        .hamburger svg {{ width: 24px; height: 24px; color: var(--text); }}
        .close-btn {{ display: none; }}
        @media (max-width: 768px) {{
            .logo img {{ height: 144px; }} .logo span {{ display: none; }}
            nav {{ position: fixed; top: 0; right: -100%; width: 250px; height: 100vh; background: var(--card); flex-direction: column; padding: 5rem 2rem; transition: right 0.3s; z-index: 1000; }}
            nav.active {{ right: 0; }}
            nav a {{ font-size: 1.1rem; padding: 0.75rem 0; border-bottom: 1px solid var(--border); width: 100%; }}
            .hamburger {{ display: block; z-index: 1001; }}
            .close-btn {{ display: block; position: absolute; top: 1rem; right: 1rem; background: none; border: none; cursor: pointer; padding: 0.5rem; }}
            .close-btn svg {{ width: 24px; height: 24px; }}
            .overlay {{ display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 999; }}
            .overlay.active {{ display: block; }}
            .stats {{ grid-template-columns: 1fr 1fr !important; }}
            .grid {{ grid-template-columns: 1fr !important; }}
        }}
        .breadcrumb {{ font-size: 0.875rem; color: var(--muted); padding: 1rem 0; }}
        .breadcrumb a {{ color: var(--primary); text-decoration: none; }}
        .hero {{ background: linear-gradient(135deg, #4B6E93 0%, #3a5775 100%); padding: 2rem; border-radius: 1rem; margin-bottom: 1.5rem; color: white; }}
        h1 {{ font-size: 1.5rem; margin-bottom: 0.5rem; font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        h1 svg {{ width: 24px; height: 24px; }}
        .subtitle {{ opacity: 0.9; margin-bottom: 1.5rem; font-size: 0.9rem; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.75rem; }}
        .stat {{ text-align: center; padding: 1rem 0.5rem; background: rgba(255,255,255,0.15); border-radius: 0.5rem; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; }}
        .stat-label {{ font-size: 0.75rem; opacity: 0.9; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1.5rem; }}
        .card {{ background: var(--card); padding: 1.5rem; border-radius: 0.75rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
        .card h3 {{ margin-bottom: 1rem; font-size: 0.9rem; color: var(--text); font-weight: 600; display: flex; align-items: center; gap: 0.5rem; }}
        .card h3 svg {{ width: 18px; height: 18px; color: var(--primary); }}
        .row {{ display: flex; justify-content: space-between; padding: 0.6rem 0; border-bottom: 1px solid var(--border); font-size: 0.875rem; }}
        .row:last-child {{ border: none; }}
        .row span:first-child {{ color: var(--muted); }}
        .row span:last-child {{ font-weight: 500; }}
        #map {{ height: 300px; border-radius: 0.75rem; margin-top: 1.5rem; }}
        .map-note {{ text-align: center; font-size: 0.75rem; color: var(--muted); margin-top: 0.5rem; }}
        .cta {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-top: 1.25rem; padding: 0.6rem 1.25rem; background: var(--accent); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        .ev-link {{ display: inline-flex; align-items: center; gap: 0.4rem; margin-left: 0.75rem; padding: 0.6rem 1.25rem; background: var(--green); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; font-size: 0.85rem; }}
        .faq {{ margin-top: 1.5rem; }}
        .faq h2 {{ font-size: 1.1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
        .faq h2 svg {{ width: 20px; height: 20px; color: var(--primary); }}
        .faq-item {{ background: var(--card); border-radius: 0.5rem; margin-bottom: 0.75rem; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
        .faq-q {{ font-weight: 600; padding: 1rem 1.25rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; font-size: 0.9rem; }}
        .faq-q:hover {{ background: #f8fafc; }}
        .faq-q svg {{ width: 16px; height: 16px; color: var(--muted); transition: transform 0.2s; }}
        .faq-item.open .faq-q svg {{ transform: rotate(180deg); }}
        .faq-a {{ padding: 0 1.25rem 1rem; font-size: 0.875rem; color: var(--muted); display: none; }}
        .faq-item.open .faq-a {{ display: block; }}
        
        .related-section {{ background: var(--card); padding: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); text-align: center; border-radius: 1rem; margin: 1.5rem 0; }}
        .related-group {{ margin-bottom: 1.25rem; }}
        .related-group:last-child {{ margin-bottom: 0; }}
        .related-group h4 {{ font-size: 0.9rem; color: var(--muted); margin-bottom: 0.75rem; font-weight: 600; }}
        .related-links {{ display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center; }}
        .related-links a {{ background: var(--bg); padding: 0.5rem 0.875rem; border-radius: 0.5rem; text-decoration: none; color: var(--text); font-size: 0.85rem; border: 1px solid var(--border); }}
        .related-links a:hover {{ border-color: var(--primary); color: var(--primary); }}
        footer {{ text-align: center; padding: 2rem 1rem; color: var(--muted); font-size: 0.875rem; margin-top: 2rem; }}
        footer a {{ color: var(--primary); text-decoration: none; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0YGF4HPVJ3"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-0YGF4HPVJ3");</script></head>
<body>
    <header>
        <div class="container header-inner">
            <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
            <button class="hamburger" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
            <div class="overlay" onclick="toggleMenu()"></div>
            <nav id="nav">
                <button class="close-btn" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M18 6L6 18M6 6l12 12"/></svg></button>
                <a href="/">Home</a>
                <a href="/routes/">Routes</a>
                <a href="/cities/">Cities</a>
                <a href="/guides/">Guides</a>
                <a href="/about/">About</a>
                <a href="/ev/" class="ev-badge">EV Trips</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <div class="breadcrumb"><a href="/">Home</a> / <a href="/routes/">Routes</a> / {from_city} to {to_city}</div>
        <div class="hero">
            <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9L18 10V6a2 2 0 00-2-2H8a2 2 0 00-2 2v4l-2.5 1.1C2.7 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg> {from_city} to {to_city}</h1>
            <p class="subtitle">via {highway}</p>
            <div class="stats">
                <div class="stat"><div class="stat-value">{time}</div><div class="stat-label">Drive Time</div></div>
                <div class="stat"><div class="stat-value">{miles}</div><div class="stat-label">Miles</div></div>
                <div class="stat"><div class="stat-value">£{petrol_cost}</div><div class="stat-label">Petrol Cost</div></div>
                <div class="stat"><div class="stat-value">£{tolls}</div><div class="stat-label">Tolls</div></div>
            </div>
            <a href="/route/{reverse_slug}/" class="cta"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M9 14l-4-4 4-4"/><path d="M5 10h11a4 4 0 110 8h-1"/></svg> Reverse</a>
            <a href="/ev/{slug}/" class="ev-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> EV Trip</a>
        </div>
        <div class="grid">
            <div class="card">
                <h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Trip Details</h3>
                <div class="row"><span>Distance</span><span>{miles} miles ({km} km)</span></div>
                <div class="row"><span>Drive Time</span><span>{time}</span></div>
                <div class="row"><span>Route</span><span>{highway}</span></div>
                <div class="row"><span>Best Time</span><span>{best_time}</span></div>
            </div>
            <div class="card">
                <h3><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 22V12a2 2 0 012-2h2a2 2 0 012 2v10M9 22V8a2 2 0 012-2h2a2 2 0 012 2v14M15 22V4a2 2 0 012-2h2a2 2 0 012 2v18"/></svg> Fuel Costs</h3>
                <div class="row"><span>Petrol (40 mpg)</span><span>~{litres} litres</span></div>
                <div class="row"><span>Est. Cost</span><span>£{petrol_cost}</span></div>
            </div>
        </div>
        <div id="map"></div>
        
        
        <div class="faq">
            <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 015.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg> Frequently Asked Questions</h2>
            <div class="faq-item open">
                <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">How long does it take to drive from {from_city} to {to_city}?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></div>
                <div class="faq-a">The drive from {from_city} to {to_city} takes approximately <strong>{time}</strong> covering {miles} miles via {highway}. Actual time may vary based on traffic, weather, and road conditions.</div>
            </div>
            <div class="faq-item">
                <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">How much does petrol cost for {from_city} to {to_city}?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></div>
                <div class="faq-a">At 40 MPG and £1.40/litre, expect to spend approximately <strong>£{petrol_cost}</strong> on petrol for this {miles}-mile trip. You'll need about {litres} litres of fuel.</div>
            </div>
            <div class="faq-item">
                <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">What is the best time to drive from {from_city} to {to_city}?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></div>
                <div class="faq-a"><strong>{best_time}</strong> to avoid heavy traffic. Weekday mornings before 7 AM or evenings after 7 PM typically have less congestion.</div>
            </div>
            <div class="faq-item">
                <div class="faq-q" onclick="this.parentElement.classList.toggle('open')">Are there tolls on the {from_city} to {to_city} route?<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg></div>
                <div class="faq-a">{toll_answer}</div>
            </div>
        </div>
    </div>
    {related_html}
    <footer><p>© 2026 <a href="/">HowLongDrive.uk</a></p></footer>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        function toggleMenu(){{document.getElementById('nav').classList.toggle('active');document.querySelector('.overlay').classList.toggle('active');}}
        
        var map = L.map('map').setView([{center_lat}, {center_lng}], {zoom});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '© OpenStreetMap'
        }}).addTo(map);
        
        var startIcon = L.divIcon({{className:'',html:'<div style="background:#4B6E93;width:24px;height:24px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3)"></div>',iconSize:[24,24],iconAnchor:[12,12]}});
        var endIcon = L.divIcon({{className:'',html:'<div style="background:#EFA24F;width:24px;height:24px;border-radius:50%;border:3px solid white;box-shadow:0 2px 6px rgba(0,0,0,0.3)"></div>',iconSize:[24,24],iconAnchor:[12,12]}});
        
        L.marker([{from_lat}, {from_lng}], {{icon: startIcon}}).addTo(map).bindPopup('<b>{from_city}</b><br>Start');
        L.marker([{to_lat}, {to_lng}], {{icon: endIcon}}).addTo(map).bindPopup('<b>{to_city}</b><br>Destination');
        
        var bounds = L.latLngBounds([[{from_lat},{from_lng}], [{to_lat},{to_lng}]]);
        map.fitBounds(bounds, {{padding: [40, 40]}});
    </script>
</body>
</html>'''

# No US highways dict needed - we use route data's highway field

best_times_short = ["Early morning (before 7 AM)", "Mid-morning (9-11 AM)", "Late evening (after 7 PM)", "Weekday mid-day"]
best_times_long = ["Early morning (before 7 AM)", "Weekday off-peak (10 AM - 3 PM)", "Sunday morning", "Late evening (after 8 PM)"]

count = 0
processed = set()

for route in routes:
    from_city = route['from']
    to_city = route['to']
    time = route['time']
    miles = route['miles']
    
    slug = f"{from_city.lower().replace(' ', '-')}-to-{to_city.lower().replace(' ', '-')}"
    if slug in processed: continue
    processed.add(slug)
    
    if from_city not in coords or to_city not in coords:
        continue
    
    reverse_slug = f"{to_city.lower().replace(' ', '-')}-to-{from_city.lower().replace(' ', '-')}"
    km = int(miles * 1.60934)
    litres = round(miles * 4.546 / 40, 1)  # miles / 40 MPG, converted to litres
    petrol_cost = round(litres * 1.40, 0)  # £1.40/litre
    petrol_cost = int(petrol_cost) if petrol_cost > 0 else 1
    highway = route.get('highway', 'A-roads')
    if miles > 100:
        best_time = best_times_long[count % len(best_times_long)]
    else:
        best_time = best_times_short[count % len(best_times_short)]
    
    # Toll answer - UK-specific
    # UK has very few toll roads: M6 Toll, Dartford Crossing, Mersey tunnels, some bridges
    m6_toll_cities = {'Birmingham', 'Birmingham Airport', 'Wolverhampton', 'Walsall', 'Tamworth',
                      'Sutton Coldfield', 'Solihull', 'West Bromwich', 'Dudley', 'Bromsgrove',
                      'Redditch', 'Kidderminster', 'Telford'}
    dartford_cities = {'Dartford', 'Gravesend', 'Basildon', 'Southend', 'Southend Airport',
                       'Chelmsford', 'Colchester', 'Ipswich', 'Norwich'}
    
    route_cities = {from_city, to_city}
    has_m6_toll = bool((route_cities & m6_toll_cities) and highway in ('M6', 'M6/M1', 'M1/M6'))
    has_dartford = bool((route_cities & dartford_cities))
    
    if has_m6_toll:
        tolls = 7
        toll_answer = f"The M6 Toll road near Birmingham charges around <strong>£{tolls}</strong> for cars. You can avoid it by using the regular M6, though expect heavier traffic."
    elif 'Dartford' in {from_city, to_city} or ('M25' in highway):
        tolls = 3
        toll_answer = "The Dartford Crossing (M25) charges <strong>£3</strong> for cars via the Dart Charge system. Register online to avoid a fine."
    else:
        tolls = 0
        toll_answer = "This route is toll-free. The UK has very few toll roads — the main ones are the M6 Toll near Birmingham and the Dartford Crossing on the M25."
    
    from_data = coords.get(from_city, {}); from_lat = from_data.get('lat', 0) if isinstance(from_data, dict) else from_data[0]; from_lng = from_data.get('lng', 0) if isinstance(from_data, dict) else from_data[1]
    to_data = coords.get(to_city, {}); to_lat = to_data.get('lat', 0) if isinstance(to_data, dict) else to_data[0]; to_lng = to_data.get('lng', 0) if isinstance(to_data, dict) else to_data[1]
    center_lat = (from_lat + to_lat) / 2
    center_lng = (from_lng + to_lng) / 2
    zoom = 5 if miles > 800 else (6 if miles > 400 else 7)
    
    os.makedirs(f'route/{slug}', exist_ok=True)
    
    # Generate Related Routes HTML
    related_html = '<div class="related-section"><h3 style="color: var(--primary); margin-bottom: 1.5rem; font-size: 1.1rem;">Related Routes</h3>'
    
    # More from same origin
    other_from = [x for x in routes_from[from_city] if x['to'] != to_city][:4]
    if other_from:
        related_html += f'<div class="related-group"><h4>More from {from_city}</h4><div class="related-links">'
        for x in other_from:
            s = f"{format_slug(from_city)}-to-{format_slug(x['to'])}"
            related_html += f'<a href="/route/{s}/">{x["to"]} ({x["time"]})</a>'
        related_html += '</div></div>'
    
    # Routes to same destination
    other_to = [x for x in routes_to[to_city] if x['from'] != from_city][:4]
    if other_to:
        related_html += f'<div class="related-group"><h4>Routes to {to_city}</h4><div class="related-links">'
        for x in other_to:
            s = f"{format_slug(x['from'])}-to-{format_slug(to_city)}"
            related_html += f'<a href="/route/{s}/">From {x["from"]} ({x["time"]})</a>'
        related_html += '</div></div>'
    
    # City hub links
    related_html += f'''<div class="related-group"><h4>Explore Cities</h4><div class="related-links">
        <a href="/cities/{format_slug(from_city)}/">All routes from {from_city}</a>
        <a href="/cities/{format_slug(to_city)}/">All routes from {to_city}</a>
    </div></div>'''
    related_html += '</div>'
    
    html = template.format(
        from_city=from_city, to_city=to_city, time=time, miles=miles,
        slug=slug, reverse_slug=reverse_slug, km=km, litres=litres,
        petrol_cost=petrol_cost, tolls=tolls, highway=highway, best_time=best_time,
        toll_answer=toll_answer,
        from_lat=from_lat, from_lng=from_lng, to_lat=to_lat, to_lng=to_lng,
        center_lat=center_lat, center_lng=center_lng, zoom=zoom,
        related_html=related_html
    )
    with open(f'route/{slug}/index.html', 'w') as f:
        f.write(html)
    count += 1

print(f"✅ Updated {count} route pages with FAQ")
