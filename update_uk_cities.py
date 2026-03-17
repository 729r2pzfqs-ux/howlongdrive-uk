import os

cities = sorted([d for d in os.listdir('cities') if os.path.isdir(f'cities/{d}')])
city_count = len(cities)

by_letter = {}
for city in cities:
    letter = city[0].upper()
    if letter not in by_letter:
        by_letter[letter] = []
    by_letter[letter].append(city)

popular = ['london', 'manchester', 'birmingham', 'edinburgh', 'glasgow', 'liverpool',
           'bristol', 'leeds', 'sheffield', 'newcastle', 'brighton', 'cardiff',
           'nottingham', 'southampton', 'oxford', 'cambridge', 'york', 'bath']

html = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UK Cities - Driving Routes | HowLongDrive</title>
    <meta name="description" content="Find driving routes from {city_count} UK cities. Calculate drive times, distances, and fuel costs.">
    <link rel="canonical" href="https://howlongdrive.uk/cities/">
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
        .stat {{ font-size: 1.25rem; font-weight: 700; color: var(--primary); margin-bottom: 1.5rem; }}
        .section {{ margin-bottom: 2rem; }}
        .section h2 {{ font-size: 1rem; margin-bottom: 1rem; color: var(--muted); border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; }}
        .section h2 svg {{ width: 20px; height: 20px; color: var(--primary); }}
        .cities-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 0.5rem; }}
        .city-card {{ background: var(--card); border-radius: 0.5rem; padding: 0.75rem 1rem; text-decoration: none; color: inherit; border: 1px solid var(--border); }}
        .city-card:hover {{ border-color: var(--primary); background: #f0f9ff; }}
        .city-name {{ font-weight: 500; font-size: 0.9rem; }}
        .letter-nav {{ display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 2rem; }}
        .letter-nav a {{ padding: 0.5rem 0.75rem; background: var(--card); border-radius: 0.25rem; text-decoration: none; color: var(--primary); font-weight: 600; border: 1px solid var(--border); }}
        .letter-nav a:hover {{ background: var(--primary); color: white; }}
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
        <h1><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 21h18M9 8h1M9 12h1M9 16h1M14 8h1M14 12h1M14 16h1M5 21V5a2 2 0 012-2h10a2 2 0 012 2v16"/></svg> UK Cities</h1>
        <p class="subtitle">Find driving routes from {city_count} UK cities</p>
        <div class="stat">{city_count} Cities</div>
        <div class="section">
            <h2><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg> Popular Cities</h2>
            <div class="cities-grid">
'''

for city in popular:
    if city in cities:
        title = city.replace('-', ' ').title()
        html += f'                <a href="/cities/{city}/" class="city-card"><span class="city-name">{title}</span></a>\n'

html += '''            </div>
        </div>
        <div class="letter-nav">
'''

for letter in sorted(by_letter.keys()):
    html += f'            <a href="#letter-{letter}">{letter}</a>\n'

html += '''        </div>
'''

for letter in sorted(by_letter.keys()):
    html += f'''        <div class="section" id="letter-{letter}">
            <h2>{letter}</h2>
            <div class="cities-grid">
'''
    for city in by_letter[letter]:
        title = city.replace('-', ' ').title()
        html += f'                <a href="/cities/{city}/" class="city-card"><span class="city-name">{title}</span></a>\n'
    html += '''            </div>
        </div>
'''

html += '''    </main>
    <footer>© 2026 <a href="/">HowLongDrive.uk</a></footer>
</body>
</html>'''

with open('cities/index.html', 'w') as f:
    f.write(html)

print(f"✅ Updated cities/index.html with {city_count} cities")
