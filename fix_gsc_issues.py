#!/usr/bin/env python3
"""Fixes for Google Search Console 'Soft 404' and 'Not found (404)' reports.

Run from the repo root. Each fix is a separate function so they can be
re-run independently; all of them are idempotent.
"""
import html
import json
import os
import re
import shutil
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

CARD = ('<a href="/route/{slug}/" class="route-card"><div>'
        '<div class="route-title">{name}</div>'
        '<div class=route-meta>{miles} miles</div></div>'
        '<div class="route-time">{time}</div></a>')

TITLE_RE = re.compile(r'<title>(.*?) Drive Time &(?:amp;)? Distance \| HowLongDrive\.uk</title>')
TIME_RE = re.compile(r'takes approximately <strong>([^<]+)</strong>')
MILES_RE = re.compile(r'<strong>[^<]+</strong> covering (\d+) miles')


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def write(p, s):
    with open(p, 'w', encoding='utf-8') as f:
        f.write(s)


def minutes(t):
    """'4h 30min' / '45min' -> integer minutes."""
    h = re.search(r'(\d+)h', t)
    m = re.search(r'(\d+)min', t)
    return (int(h.group(1)) * 60 if h else 0) + (int(m.group(1)) if m else 0)


def route_data(slug):
    """Pull destination name, miles and drive time out of a built route page."""
    p = os.path.join('route', slug, 'index.html')
    if not os.path.isfile(p):
        return None
    h = read(p)
    t = TITLE_RE.search(h)
    tm = TIME_RE.search(h)
    mi = MILES_RE.search(h)
    if not (t and tm and mi):
        return None
    pair = html.unescape(t.group(1))
    if ' to ' not in pair:
        return None
    dest = pair.split(' to ', 1)[1]
    return {'slug': slug, 'name': dest, 'time': tm.group(1),
            'miles': int(mi.group(1)), 'mins': minutes(tm.group(1))}


# --------------------------------------------------------------------------
# Fix 1 - delete the literal {search_term} directory created from the
# WebSite SearchAction urlTemplate. Live 200 + meta-refresh to home = soft 404.
# --------------------------------------------------------------------------
def fix_search_term():
    for d in ('route/{search_term}', 'route/(search_term)'):
        if os.path.isdir(d):
            shutil.rmtree(d)
            print(f'  removed {d}/')
        else:
            print(f'  {d}/ already gone')


# --------------------------------------------------------------------------
# Fix 2 - the three landmark city pages render empty <div class="routes-grid">
# because their route pages live under apostrophe slugs (hadrian's-wall)
# while the city page looked them up as hadrians-wall.
# --------------------------------------------------------------------------
LANDMARKS = {
    'hadrians-wall': "hadrian's-wall",
    'giants-causeway': "giant's-causeway",
    'lands-end': "land's-end",
}

SHORT_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
              'style="width:18px;height:18px;vertical-align:middle;margin-right:4px">'
              '<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9L18 10V6a2 2 0 00-2-2H8a2 '
              '2 0 00-2 2v4l-2.5 1.1C2.7 11.3 2 12.1 2 13v3c0 .6.4 1 1 1h2"/>'
              '<circle cx="7" cy="17" r="2"/><circle cx="17" cy="17" r="2"/></svg>')
MEDIUM_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
               'style="width:18px;height:18px;vertical-align:middle;margin-right:4px">'
               '<path d="M4 19L9 2h6l5 17"/><path d="M12 2v17"/></svg>')
LONG_ICON = MEDIUM_ICON
H3 = ('<h3 style="margin:1.5rem 0 0.75rem;font-size:0.95rem;color:var(--primary)">'
      '{icon} {label} — {n} routes</h3>')


def landmark_routes(apos):
    """All routes departing the landmark, sorted by distance."""
    out = []
    prefix = apos + '-to-'
    for d in os.listdir('route'):
        if d.startswith(prefix):
            r = route_data(d)
            if r:
                out.append(r)
    out.sort(key=lambda r: r['miles'])
    return out


def build_sections(routes):
    buckets = [('Short Drives (under 3 hours)', SHORT_ICON, [r for r in routes if r['mins'] < 180]),
               ('Medium Trips (3–6 hours)', MEDIUM_ICON, [r for r in routes if 180 <= r['mins'] < 360]),
               ('Long Journeys (6+ hours)', LONG_ICON, [r for r in routes if r['mins'] >= 360])]
    parts = []
    for label, icon, rs in buckets:
        if not rs:
            continue
        parts.append(H3.format(icon=icon, label=label, n=len(rs)).replace('— 1 routes', '— 1 route'))
        cards = '\n            '.join(CARD.format(**r) for r in rs)
        parts.append('<div class="routes-grid">' + cards + '</div>')
    return '\n        '.join(parts)


def fix_landmark_cities():
    for city, apos in LANDMARKS.items():
        p = f'cities/{city}/index.html'
        h = read(p)
        routes = landmark_routes(apos)
        if not routes:
            print(f'  !! {city}: no source routes found, skipped')
            continue
        section = build_sections(routes)

        # Replace everything from the first bucket <h3> (or the bare grid, for
        # the lands-end template) through the final routes-grid close tag.
        start = h.find('<h3 style="margin:1.5rem 0 0.75rem')
        if start == -1:
            start = h.find('<div class="routes-grid">')
        # Find the end of the last routes-grid block.
        last = h.rfind('<div class="routes-grid">')
        end = h.find('</div>', last) + len('</div>')
        if start == -1 or last == -1 or end <= start:
            print(f'  !! {city}: could not locate route grid, skipped')
            continue
        h = h[:start] + section + h[end:]

        n = len(routes)
        names = [r['name'] for r in routes]
        h = update_counts(h, city, n, names, routes)
        write(p, h)
        print(f'  {city}: injected {n} route cards')


# --------------------------------------------------------------------------
# Fix 4a - counts shared by the landmark fix and the dedupe fix.
# --------------------------------------------------------------------------
def update_counts(h, city, n, names, routes):
    """Re-sync every place a route/destination count is printed."""
    h = re.sub(r'(<div class="stat-value">)\d+(</div><div class="stat-label">Destinations)',
               rf'\g<1>{n}\g<2>', h)
    h = re.sub(r'\d+ destinations sorted by distance', f'{n} destinations sorted by distance', h)
    h = re.sub(r'(Browse |Find driving times and distances from [^.]*? to )\d+( routes| destinations)',
               rf'\g<1>{n}\g<2>', h)
    h = re.sub(r'\b\d+( driving routes from )', rf'{n}\g<1>', h)
    h = re.sub(r'\b\d+( routes with distances)', rf'{n}\g<1>', h)
    h = re.sub(r'\b\d+( routes with accurate travel times)', rf'{n}\g<1>', h)
    h = re.sub(r'(has )\d+( routes in our database)', rf'\g<1>{n}\g<2>', h)
    h = re.sub(r'(There are )\d+( cities within 2 hours)', rf'\g<1>{n}\g<2>', h)

    # "including A, B, C" - dedupe and cap at three.
    near = [r['name'] for r in routes if r['mins'] < 120]
    seen, uniq = set(), []
    for x in near or names:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    inc = ', '.join(uniq[:3])
    if inc:
        h = re.sub(r'(within 2 hours[^<"]*?, including )[^.<"]+(\.)', rf'\g<1>{inc}\g<2>', h)
    # "Popular: London, London." / "Popular destinations include A, A, B."
    def dedupe_list(m):
        seen, out = set(), []
        for x in [s.strip() for s in m.group(2).split(',')]:
            if x and x not in seen:
                seen.add(x)
                out.append(x)
        return m.group(1) + ', '.join(out[:3]) + m.group(3)

    h = re.sub(r'(Popular(?: destinations include)?: ?)([^.<"]+)(\.)', dedupe_list, h)
    h = re.sub(r'(Popular destinations include )([^.<"]+)(\.)', dedupe_list, h)

    if n == 1:
        for a, b in (('There are 1 cities within 2 hours', 'There is 1 city within 2 hours'),
                     ('has 1 routes in our database', 'has 1 route in our database'),
                     ('1 destinations sorted by distance', '1 destination sorted by distance'),
                     ('1 routes with', '1 route with'),
                     ('1 driving routes from', '1 driving route from'),
                     ('Browse 1 routes', 'Browse 1 route'),
                     ('<div class="stat-label">Destinations</div>',
                      '<div class="stat-label">Destination</div>'),
                     ('to 1 destinations', 'to 1 destination')):
            h = h.replace(a, b)
    return h


# --------------------------------------------------------------------------
# Fix 3 - remove internal links whose target page was never built.
# --------------------------------------------------------------------------
def all_pages():
    for r, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in ('.git', 'assets', 'data')]
        for f in files:
            if f.endswith('.html'):
                yield os.path.join(r, f)


def collect_broken():
    targets = set()
    for base in ('route', 'ev'):
        for d in os.listdir(base):
            if os.path.isfile(os.path.join(base, d, 'index.html')):
                targets.add(f'/{base}/{d}/')
    broken = set()
    for p in all_pages():
        for m in re.findall(r'href="(/(?:route|ev)/[^"]+/)"', read(p)):
            if m not in targets:
                broken.add(m)
    return broken


def fix_broken_links():
    broken = collect_broken()
    print(f'  {len(broken)} broken targets: {sorted(broken)}')
    if not broken:
        return
    pat = re.compile(r'\s*<a href="(' + '|'.join(re.escape(b) for b in sorted(broken)) + r')"[^>]*>.*?</a>', re.S)
    changed = 0
    for p in all_pages():
        h = read(p)
        if not any(b in h for b in broken):
            continue
        h2 = pat.sub('', h)
        if h2 != h:
            write(p, h2)
            changed += 1
    print(f'  removed dead anchors from {changed} pages')


# --------------------------------------------------------------------------
# Fix 5 - stop linking to the 131 meta-refresh stubs; point straight at the
# apostrophe canonical they redirect to.
# --------------------------------------------------------------------------
REFRESH_RE = re.compile(r'refresh" content="0;\s*url=([^"]+)"')


def stub_map():
    """{'/route/leeds-to-hadrians-wall/': "/route/leeds-to-hadrian's-wall/"}"""
    out = {}
    for base in ('route', 'ev'):
        for d in os.listdir(base):
            p = os.path.join(base, d, 'index.html')
            if not os.path.isfile(p) or os.path.getsize(p) > 2500:
                continue
            m = REFRESH_RE.search(read(p))
            if m:
                out[f'/{base}/{d}/'] = re.sub(r'^https://howlongdrive\.uk', '', m.group(1))
    return out


def apostrophe_twin(base, slug):
    """hadrians-wall -> hadrian's-wall etc. Returns the real page's slug or None."""
    for bad, good in (('hadrians-wall', "hadrian's-wall"),
                      ('giants-causeway', "giant's-causeway"),
                      ('lands-end', "land's-end"),
                      ('john-ogroats', "john-o'groats")):
        if bad in slug:
            cand = slug.replace(bad, good)
            if os.path.isfile(os.path.join(base, cand, 'index.html')):
                return cand
    return None


def fix_generic_stubs():
    """Stubs that meta-refresh to the homepage or the /routes/ hub are soft 404s.

    Point them at the real apostrophe page where one exists; otherwise delete the
    directory so the URL returns an honest 404 instead of a 200.
    """
    repointed = removed = 0
    for base in ('route', 'ev'):
        for d in sorted(os.listdir(base)):
            p = os.path.join(base, d, 'index.html')
            if not os.path.isfile(p) or os.path.getsize(p) > 2500:
                continue
            h = read(p)
            m = REFRESH_RE.search(h)
            if not m:
                continue
            target = re.sub(r'^https://howlongdrive\.uk', '', m.group(1))
            if target not in ('/', '/routes/', '/ev/'):
                continue
            twin = apostrophe_twin(base, d)
            if twin:
                good = f'/{base}/{twin}/'
                h = REFRESH_RE.sub(f'refresh" content="0; url={good}"', h)
                h = re.sub(r'<link rel="canonical" href="[^"]*"',
                           f'<link rel="canonical" href="https://howlongdrive.uk{good}"', h)
                if '<title>' not in h:
                    h = h.replace('</head>', '<title>Redirecting...</title></head>', 1)
                write(p, h)
                repointed += 1
            else:
                shutil.rmtree(os.path.join(base, d))
                removed += 1
                print(f'    deleted {base}/{d}/ (redirected to {target}, no real page)')
    print(f'  repointed {repointed} generic stubs, deleted {removed}')


def fix_stub_links():
    mapping = stub_map()
    print(f'  {len(mapping)} redirect stubs found')
    changed = 0
    for p in all_pages():
        h = read(p)
        if REFRESH_RE.search(h):
            continue  # don't rewrite the stubs themselves
        orig = h
        for stub, target in mapping.items():
            if f'href="{stub}"' in h:
                h = h.replace(f'href="{stub}"', f'href="{target}"')
        if h != orig:
            write(p, h)
            changed += 1
    print(f'  repointed stub links on {changed} pages')
    return mapping


# --------------------------------------------------------------------------
# Fix 4 - dedupe bidirectional route pairs on city pages, then noindex the
# city pages that are still left with <=2 destinations.
# --------------------------------------------------------------------------
NOINDEX = '<meta name="robots" content="noindex,follow">'


def fix_city_pages(skip):
    deduped = noindexed = 0
    thin = []
    for d in sorted(os.listdir('cities')):
        p = f'cities/{d}/index.html'
        if not os.path.isfile(p):
            continue
        h = read(p)
        cards = re.findall(r'<a href="(/route/([^"]+?)/)" class="route-card">.*?</a>', h, re.S)
        # Drop a card when the same journey already appears in the other direction.
        seen_pairs, drop = set(), []
        for href, slug in cards:
            if '-to-' not in slug:
                continue
            a, b = slug.split('-to-', 1)
            key = tuple(sorted((a, b)))
            if key in seen_pairs:
                drop.append(href)
            else:
                seen_pairs.add(key)
        if drop:
            for href in drop:
                h = re.sub(r'\s*<a href="' + re.escape(href) + r'" class="route-card">.*?</a>',
                           '', h, count=1, flags=re.S)
            deduped += 1

        # Recount from what is actually rendered now.
        remaining = re.findall(r'<a href="/route/([^"]+?)/" class="route-card">(.*?)</a>', h, re.S)
        n = len(remaining)
        if n and d not in skip:
            routes = []
            for slug, body in remaining:
                nm = re.search(r'route-title">([^<]+)<', body)
                tm = re.search(r'route-time">([^<]+)<', body)
                routes.append({'name': html.unescape(nm.group(1)) if nm else '',
                               'mins': minutes(tm.group(1)) if tm else 0})
            h = update_counts(h, d, n, [r['name'] for r in routes], routes)
            # Bucket headings ("Short Drives — 2").
            h = fix_bucket_headings(h)

        if n <= 2 and NOINDEX not in h:
            h = h.replace('<link rel="canonical"', NOINDEX + '\n    <link rel="canonical"', 1)
            noindexed += 1
            thin.append((d, n))
        write(p, h)
    print(f'  deduped {deduped} city pages; noindexed {noindexed} thin pages')
    print(f'  thin: {thin}')
    prune_sitemap([d for d, _ in thin])


def prune_sitemap(slugs):
    """A noindexed URL must not stay in the sitemap."""
    p = 'sitemap-cities.xml'
    h = read(p)
    before = h.count('<loc>')
    for s in slugs:
        h = re.sub(r'<url>\s*<loc>https://howlongdrive\.uk/cities/' + re.escape(s) +
                   r'/</loc>.*?</url>\s*', '', h, flags=re.S)
    write(p, h)
    print(f'  sitemap-cities.xml: {before} -> {h.count("<loc>")} URLs')


def fix_bucket_headings(h):
    """Recount each 'Short Drives — N' heading from the cards that follow it.

    A bucket emptied by the dedupe loses both its heading and its now-empty
    routes-grid, so we never reintroduce the empty-grid soft 404.
    """
    parts = re.split(r'(<h3 style="margin:1\.5rem 0 0\.75rem.*?</h3>)', h, flags=re.S)
    for i in range(1, len(parts), 2):
        head = parts[i]
        body = parts[i + 1] if i + 1 < len(parts) else ''
        cnt = len(re.findall(r'class="route-card"', body))
        if cnt:
            word = ' route' if cnt == 1 else ' routes'
            parts[i] = re.sub(r'— \d+(?: routes?)?</h3>',
                              f'— {cnt}' + (word if re.search(r'routes?</h3>', head) else '') + '</h3>',
                              head)
        else:
            parts[i] = ''
            parts[i + 1] = re.sub(r'\s*<div class="routes-grid">\s*</div>', '', body)
    return ''.join(parts)


if __name__ == '__main__':
    steps = sys.argv[1:] or ['1', '2', '3', '5', '4']
    if '1' in steps:
        print('Fix 1: {search_term}')
        fix_search_term()
    if '2' in steps:
        print('Fix 2: landmark city pages')
        fix_landmark_cities()
    if '3' in steps:
        print('Fix 3: broken internal links')
        fix_broken_links()
    if '5' in steps:
        print('Fix 5: redirect stubs')
        fix_generic_stubs()
        fix_stub_links()
        print('Fix 3 (rerun): links to any stub deleted above')
        fix_broken_links()
    if '4' in steps:
        print('Fix 4: city dedupe + noindex')
        fix_city_pages(skip=set(LANDMARKS))
