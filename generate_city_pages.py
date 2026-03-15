import json
import os
from collections import defaultdict

# Load all routes
routes = []
for f in ['data/routes.json', 'data/routes_expanded.json', 'data/routes_commute.json', 'data/routes_tourist.json', 'data/routes_airport.json', 'data/routes_small_cities.json']:
    if os.path.exists(f):
        with open(f, 'r') as file:
            routes.extend(json.load(file))

# Group routes by FROM city
city_routes = defaultdict(list)
for r in routes:
    city_routes[r['from']].append(r)

# City metadata
city_states = {
    "New York": "New York", "Los Angeles": "California", "Chicago": "Illinois",
    "Houston": "Texas", "Phoenix": "Arizona", "Philadelphia": "Pennsylvania",
    "San Antonio": "Texas", "San Diego": "California", "Dallas": "Texas",
    "San Jose": "California", "Austin": "Texas", "Jacksonville": "Florida",
    "San Francisco": "California", "Seattle": "Washington", "Denver": "Colorado",
    "Washington DC": "District of Columbia", "Boston": "Massachusetts",
    "Nashville": "Tennessee", "Detroit": "Michigan", "Portland": "Oregon",
    "Las Vegas": "Nevada", "Miami": "Florida", "Atlanta": "Georgia",
    "Minneapolis": "Minnesota", "Orlando": "Florida", "Tampa": "Florida",
    "Salt Lake City": "Utah", "New Orleans": "Louisiana", "Cleveland": "Ohio",
    "Kansas City": "Missouri", "Columbus": "Ohio", "Indianapolis": "Indiana",
    "Charlotte": "North Carolina", "Raleigh": "North Carolina", "Memphis": "Tennessee",
    "Baltimore": "Maryland", "Milwaukee": "Wisconsin", "Albuquerque": "New Mexico",
    "Tucson": "Arizona", "Fresno": "California", "Sacramento": "California",
    "Oklahoma City": "Oklahoma", "El Paso": "Texas", "St Louis": "Missouri",
    "Pittsburgh": "Pennsylvania", "Cincinnati": "Ohio", "Spokane": "Washington",
    "Reno": "Nevada", "Colorado Springs": "Colorado", "Vancouver": "Washington",
    "Albany": "New York", "Hartford": "Connecticut", "Providence": "Rhode Island",
    "Little Rock": "Arkansas"
}

template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driving Times from {city} - Routes & Distances | HowLongDrive</title>
    <meta name="description" content="Find driving times from {city}, {state} to other cities. Browse {route_count} routes with distances, drive times, and trip costs.">
    <link rel="canonical" href="https://howlongdrive.uk/city/{slug}/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <meta name="theme-color" content="#4B6E93">
    <meta property="og:title" content="Driving Times from {city}">
    <meta property="og:description" content="Find driving times from {city} to other cities">
    <meta property="og:image" content="https://howlongdrive.uk/assets/og-image.png">
    <style>
        :root {{ --primary: #4B6E93; --accent: #EFA24F; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; --green: #10B981; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 1000px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.75rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-weight: 700; font-size: 1.5rem; color: var(--primary); text-decoration: none; display: flex; align-items: center; gap: 0.75rem; }}
        .logo img {{ height: 100px; width: auto; }}
        nav {{ display: flex; align-items: center; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--green); color: white; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; font-weight: 600; }}
        .hamburger {{ display: none; background: none; border: none; cursor: pointer; padding: 0.5rem; }}
        .close-btn {{ display: none; }}
        @media (max-width: 768px) {{
            .logo img {{ height: 60px; }} .logo span {{ display: none; }}
            nav {{ position: fixed; top: 0; right: -100%; width: 250px; height: 100vh; background: var(--card); flex-direction: column; padding: 5rem 2rem; transition: right 0.3s; z-index: 1000; }}
            nav.active {{ right: 0; }}
            .hamburger {{ display: block; z-index: 1001; }}
            .close-btn {{ display: block; position: absolute; top: 1rem; right: 1rem; background: none; border: none; cursor: pointer; }}
            .overlay {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 999; }}
            .overlay.active {{ display: block; }}
        }}
        .hero {{ background: var(--card); padding: 2rem; border-radius: 1rem; margin: 1.5rem 0; text-align: center; }}
        h1 {{ font-size: 2rem; margin-bottom: 0.5rem; display: flex; align-items: center; justify-content: center; gap: 0.75rem; }}
        h1 svg {{ width: 32px; height: 32px; color: var(--primary); }}
        .subtitle {{ color: var(--muted); }}
        .stats {{ display: flex; justify-content: center; gap: 2rem; margin-top: 1.5rem; }}
        .stat {{ text-align: center; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; color: var(--primary); }}
        .stat-label {{ font-size: 0.875rem; color: var(--muted); }}
        .routes-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; margin: 1.5rem 0; }}
        .route-card {{ background: var(--card); border-radius: 0.75rem; padding: 1.25rem; text-decoration: none; color: inherit; border: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }}
        .route-card:hover {{ border-color: var(--primary); }}
        .route-title {{ font-weight: 600; }}
        .route-meta {{ color: var(--muted); font-size: 0.875rem; margin-top: 0.25rem; }}
        .route-time {{ font-weight: 600; color: var(--primary); font-size: 1.1rem; }}
        .ev-link {{ display: inline-flex; align-items: center; gap: 0.5rem; margin-top: 2rem; padding: 0.75rem 1.5rem; background: var(--green); color: white; border-radius: 0.5rem; text-decoration: none; font-weight: 600; }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; margin-top: 2rem; }}
        footer a {{ color: var(--primary); text-decoration: none; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-NXC7PNTC4G"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag("js",new Date());gtag("config","G-NXC7PNTC4G");</script></head>
<body>
    <header>
        <div class="container header-inner">
            <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"><span>HowLongDrive</span></a>
            <button class="hamburger" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M3 12h18M3 6h18M3 18h18"/></svg></button>
            <div class="overlay" onclick="toggleMenu()"></div>
            <nav id="nav">
                <button class="close-btn" style="display:none" onclick="toggleMenu()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:24px;height:24px"><path d="M18 6L6 18M6 6l12 12"/></svg></button>
                <a href="/">Home</a>
                <a href="/routes/">Routes</a>
                <a href="/cities/">Cities</a>
                <a href="/ev/" class="ev-badge">EV Trips</a>
            </nav>
        </div>
    </header>
    <div class="container">
        <div class="hero">
            <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="10" r="3"/><path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 10-16 0c0 3 2.7 7 8 11.7z"/></svg> {city}</h1>
            <p class="subtitle">{state}</p>
            <div class="stats">
                <div class="stat"><div class="stat-value">{route_count}</div><div class="stat-label">Destinations</div></div>
            </div>
        </div>
        
        <h2 style="margin-bottom:1rem">Driving Times from {city}</h2>
        <div class="routes-grid">
            {routes_html}
        </div>
        
        <div style="text-align:center">
            <a href="/ev/" class="ev-link"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:20px;height:20px"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg> Plan EV Trip from {city}</a>
        </div>
    </div>
    <footer><p>© 2026 <a href="/">HowLongDrive.uk</a></p></footer>
    <script>function toggleMenu(){{document.getElementById('nav').classList.toggle('active');document.querySelector('.overlay').classList.toggle('active');}}</script>
</body>
</html>'''

# Generate city pages
os.makedirs('city', exist_ok=True)
count = 0

for city, city_route_list in city_routes.items():
    if len(city_route_list) < 2:  # Skip cities with only 1 route
        continue
    
    slug = city.lower().replace(' ', '-')
    state = city_states.get(city, "USA")
    
    # Sort routes by distance
    city_route_list.sort(key=lambda x: x['miles'])
    
    routes_html = ""
    for r in city_route_list:
        to_slug = f"{city.lower().replace(' ', '-')}-to-{r['to'].lower().replace(' ', '-')}"
        routes_html += f'''
            <a href="/route/{to_slug}/" class="route-card">
                <div>
                    <div class="route-title">{r['to']}</div>
                    <div class="route-meta">{r['miles']} miles</div>
                </div>
                <div class="route-time">{r['time']}</div>
            </a>'''
    
    os.makedirs(f'city/{slug}', exist_ok=True)
    html = template.format(
        city=city, state=state, slug=slug,
        route_count=len(city_route_list),
        routes_html=routes_html
    )
    
    with open(f'city/{slug}/index.html', 'w') as f:
        f.write(html)
    count += 1
    print(f"✅ {city} ({len(city_route_list)} routes)")

print(f"\n✅ Created {count} city hub pages")
