import os

route_count = len([d for d in os.listdir('route') if os.path.isdir(f'route/{d}')])
ev_count = len([d for d in os.listdir('ev') if os.path.isdir(f'ev/{d}')])
city_count = len([d for d in os.listdir('cities') if os.path.isdir(f'cities/{d}')])

popular = [
    ('london-to-manchester', 'London', 'Manchester', '4h', '200 mi'),
    ('london-to-edinburgh', 'London', 'Edinburgh', '7h', '400 mi'),
    ('london-to-birmingham', 'London', 'Birmingham', '2h', '120 mi'),
    ('manchester-to-liverpool', 'Manchester', 'Liverpool', '1h', '35 mi'),
    ('london-to-bristol', 'London', 'Bristol', '2h', '120 mi'),
    ('london-to-brighton', 'London', 'Brighton', '1h 30m', '55 mi'),
    ('london-to-cambridge', 'London', 'Cambridge', '1h 30m', '60 mi'),
    ('london-to-oxford', 'London', 'Oxford', '1h 30m', '60 mi'),
    ('birmingham-to-manchester', 'Birmingham', 'Manchester', '1h 30m', '85 mi'),
    ('edinburgh-to-glasgow', 'Edinburgh', 'Glasgow', '1h', '45 mi'),
]

html = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driving Routes & Road Trips UK | HowLongDrive</title>
    <meta name="description" content="Find driving times for {route_count:,}+ routes across the UK. Calculate drive time, fuel costs, and plan road trips.">
    <link rel="canonical" href="https://howlongdrive.uk/routes/">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">
    <style>
        :root {{ --primary: #4B6E93; --green: #10B981; --bg: #f8fafc; --card: #fff; --text: #1e293b; --muted: #64748b; --border: #e2e8f0; }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
        .container {{ max-width: 1100px; margin: 0 auto; padding: 0 1rem; }}
        header {{ background: var(--card); border-bottom: 1px solid var(--border); padding: 0.25rem 0; }}
        .header-inner {{ display: flex; justify-content: space-between; align-items: center; }}
        .logo img {{ height: 180px; }}
        nav {{ display: flex; gap: 1.5rem; }}
        nav a {{ color: var(--muted); text-decoration: none; font-size: 0.875rem; }}
        .ev-badge {{ background: var(--green); color: #fff; padding: 0.25rem 0.75rem; border-radius: 1rem; font-size: 0.75rem; }}
        @media (max-width: 768px) {{ .logo img {{ height: 144px; }} nav {{ display: none; }} }}
        h1 {{ font-size: 2rem; margin: 2rem 0 0.5rem; display: flex; align-items: center; gap: 0.75rem; }}
        h1 svg {{ width: 32px; height: 32px; color: var(--primary); }}
        .subtitle {{ color: var(--muted); margin-bottom: 1.5rem; }}
        .stats {{ display: flex; gap: 2rem; margin: 1rem 0 2rem; flex-wrap: wrap; }}
        .stat-value {{ font-size: 1.5rem; font-weight: 700; color: var(--primary); }}
        .stat-label {{ font-size: 0.8rem; color: var(--muted); }}
        .section {{ margin-bottom: 2.5rem; }}
        .section h2 {{ font-size: 1.1rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }}
        .section h2 svg {{ width: 20px; height: 20px; color: var(--primary); }}
        .routes-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 0.75rem; }}
        .route-card {{ background: var(--card); border-radius: 0.5rem; padding: 1rem; text-decoration: none; color: inherit; border: 1px solid var(--border); }}
        .route-card:hover {{ border-color: var(--primary); }}
        .route-title {{ font-weight: 600; font-size: 0.95rem; }}
        .route-meta {{ color: var(--muted); font-size: 0.8rem; margin-top: 0.25rem; }}
        footer {{ text-align: center; padding: 2rem; color: var(--muted); font-size: 0.875rem; }}
    </style>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-0YGF4HPVJ3"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","G-0YGF4HPVJ3")</script>
</head>
<body>
    <header><div class="container header-inner">
        <a href="/" class="logo"><img src="/assets/logo-header.png" alt="HowLongDrive"></a>
        <nav><a href="/">Home</a><a href="/routes/">Routes</a><a href="/cities/">Cities</a><a href="/guides/">Guides</a><a href="/ev/" class="ev-badge">⚡ EV Trips</a><a href="/about/">About</a></nav>
    </div></header>
    <main class="container">
        <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg> Driving Routes</h1>
        <p class="subtitle">Find driving times and distances for {route_count:,}+ routes across the UK</p>
        <div class="stats">
            <div class="stat"><div class="stat-value">{route_count:,}</div><div class="stat-label">Routes</div></div>
            <div class="stat"><div class="stat-value">{ev_count:,}</div><div class="stat-label">EV Routes</div></div>
            <div class="stat"><div class="stat-value">{city_count}</div><div class="stat-label">Cities</div></div>
        </div>
        <div class="section">
            <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Popular Routes</h2>
            <div class="routes-grid">
'''

for slug, from_city, to_city, time, dist in popular:
    html += f'''                <a href="/route/{slug}/" class="route-card">
                    <div class="route-title">{from_city} → {to_city}</div>
                    <div class="route-meta">{time} • {dist}</div>
                </a>
'''

html += '''            </div>
        </div>
    </main>
    <footer>© 2026 <a href="/">HowLongDrive.uk</a></footer>
</body>
</html>'''

with open('routes/index.html', 'w') as f:
    f.write(html)

print(f"✅ Updated routes/index.html: {route_count:,} routes, {ev_count:,} EV, {city_count} cities")
