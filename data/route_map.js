const ROUTE_MAP = {
  "London": [
    "Barking",
    "Bath",
    "Birmingham",
    "Bournemouth",
    "Brighton",
    "Bristol",
    "Bromley",
    "Cambridge",
    "Cardiff",
    "Chelmsford",
    "Coventry",
    "Croydon",
    "Dartford",
    "Ealing",
    "Edinburgh",
    "Enfield",
    "Epsom",
    "Exeter",
    "Gatwick Airport",
    "Glasgow",
    "Gravesend",
    "Guildford",
    "Harrow",
    "Heathrow Airport",
    "Ilford",
    "Ipswich",
    "Kingston",
    "Leeds",
    "Leicester",
    "Liverpool",
    "Luton",
    "Luton Airport",
    "Manchester",
    "Milton Keynes",
    "Newcastle",
    "Northampton",
    "Norwich",
    "Nottingham",
    "Oxford",
    "Plymouth",
    "Portsmouth",
    "Reading",
    "Richmond",
    "Romford",
    "Sevenoaks",
    "Sheffield",
    "Slough",
    "Southampton",
    "St Albans",
    "Stansted Airport",
    "Sunderland",
    "Swansea",
    "Swindon",
    "Watford",
    "Wembley",
    "Wimbledon",
    "Woking",
    "York"
  ],
  "Birmingham": [
    "Birmingham Airport",
    "Bristol",
    "Bromsgrove",
    "Cardiff",
    "Coventry",
    "Derby",
    "Dudley",
    "Leeds",
    "Leicester",
    "Liverpool",
    "London",
    "Manchester",
    "Milton Keynes",
    "Northampton",
    "Nottingham",
    "Redditch",
    "Sheffield",
    "Solihull",
    "Stoke-on-Trent",
    "Sutton Coldfield",
    "Swansea",
    "Tamworth",
    "Walsall",
    "West Bromwich",
    "Wolverhampton",
    "Worcester"
  ],
  "Manchester": [
    "Altrincham",
    "Birmingham",
    "Blackpool",
    "Bolton",
    "Bradford",
    "Bury",
    "Chester",
    "Derby",
    "Edinburgh",
    "Glasgow",
    "Lake District",
    "Leeds",
    "Leeds Bradford Airport",
    "Liverpool",
    "Liverpool Airport",
    "London",
    "Macclesfield",
    "Manchester Airport",
    "Newcastle",
    "Oldham",
    "Preston",
    "Rochdale",
    "Salford",
    "Sheffield",
    "Stockport",
    "Stoke-on-Trent",
    "Warrington",
    "Wigan",
    "Wolverhampton",
    "York"
  ],
  "Liverpool": [
    "Belfast",
    "Birkenhead",
    "Birmingham",
    "Blackpool",
    "Bootle",
    "Chester",
    "Leeds",
    "Liverpool Airport",
    "London",
    "Manchester",
    "Preston",
    "Southport",
    "St Helens",
    "Widnes"
  ],
  "Leeds": [
    "Bradford",
    "Dewsbury",
    "Halifax",
    "Harrogate",
    "Huddersfield",
    "Hull",
    "Leeds Bradford Airport",
    "London",
    "Manchester",
    "Middlesbrough",
    "Newcastle",
    "Otley",
    "Pudsey",
    "Sheffield",
    "Wakefield",
    "Wetherby",
    "York"
  ],
  "Edinburgh": [
    "Aberdeen",
    "Belfast",
    "Dalkeith",
    "Dundee",
    "Dunfermline",
    "Edinburgh Airport",
    "Glasgow",
    "Inverness",
    "Kirkcaldy",
    "Livingston",
    "London",
    "Manchester",
    "Musselburgh",
    "Newcastle",
    "Newcastle Airport",
    "Perth",
    "Stirling"
  ],
  "Glasgow": [
    "Aberdeen",
    "Belfast",
    "Clydebank",
    "Coatbridge",
    "Dumbarton",
    "Dundee",
    "East Kilbride",
    "Edinburgh",
    "Glasgow Airport",
    "Hamilton",
    "Inverness",
    "London",
    "Manchester",
    "Motherwell",
    "Paisley",
    "Perth",
    "Stirling"
  ],
  "Bristol": [
    "Bath",
    "Birmingham",
    "Bristol Airport",
    "Cardiff",
    "Clevedon",
    "Exeter",
    "Filton",
    "Gloucester",
    "Keynsham",
    "London",
    "Portishead",
    "Swansea",
    "Swindon",
    "Thornbury",
    "Weston-super-Mare"
  ],
  "Cardiff": [
    "Birmingham",
    "Bristol",
    "London",
    "Newport",
    "Swansea"
  ],
  "Newcastle": [
    "Durham",
    "Edinburgh",
    "Leeds",
    "London",
    "Manchester",
    "Middlesbrough",
    "Newcastle Airport",
    "Sunderland",
    "York"
  ],
  "Sheffield": [
    "Birmingham",
    "Bradford",
    "Derby",
    "Doncaster",
    "Leeds",
    "London",
    "Manchester",
    "Nottingham",
    "Stoke-on-Trent",
    "York"
  ],
  "Nottingham": [
    "Birmingham",
    "Coventry",
    "Derby",
    "Leicester",
    "Lincoln",
    "London",
    "Sheffield",
    "Stoke-on-Trent"
  ],
  "Leicester": [
    "Birmingham",
    "Coventry",
    "Derby",
    "London",
    "Milton Keynes",
    "Northampton",
    "Nottingham"
  ],
  "Cambridge": [
    "Ipswich",
    "London",
    "Luton",
    "Milton Keynes",
    "Northampton",
    "Norwich",
    "Oxford",
    "Peterborough",
    "Stansted Airport"
  ],
  "Oxford": [
    "Birmingham",
    "Bristol",
    "Cambridge",
    "London",
    "Milton Keynes",
    "Northampton",
    "Reading",
    "Swindon"
  ],
  "Brighton": [
    "Gatwick Airport",
    "London",
    "Portsmouth",
    "Southampton"
  ],
  "Southampton": [
    "Bournemouth",
    "Brighton",
    "Bristol",
    "London",
    "Portsmouth"
  ],
  "York": [
    "Bradford",
    "Hull",
    "Leeds",
    "London",
    "Manchester",
    "Newcastle",
    "Scarborough"
  ],
  "Exeter": [
    "Bristol",
    "London",
    "Plymouth",
    "Torquay"
  ],
  "Plymouth": [
    "Bristol",
    "Exeter",
    "London",
    "Newquay",
    "Penzance"
  ],
  "Watford": [
    "London"
  ],
  "Croydon": [
    "London"
  ],
  "Bromley": [
    "London"
  ],
  "Enfield": [
    "London"
  ],
  "Romford": [
    "London"
  ],
  "Ilford": [
    "London"
  ],
  "Barking": [
    "London"
  ],
  "Wimbledon": [
    "London"
  ],
  "Kingston": [
    "London"
  ],
  "Richmond": [
    "London"
  ],
  "Ealing": [
    "London"
  ],
  "Harrow": [
    "London"
  ],
  "Wembley": [
    "London"
  ],
  "Slough": [
    "London",
    "Reading"
  ],
  "Reading": [
    "Basingstoke",
    "London",
    "Newbury",
    "Oxford",
    "Slough",
    "Swindon"
  ],
  "Guildford": [
    "London"
  ],
  "Woking": [
    "London"
  ],
  "St Albans": [
    "London",
    "Luton"
  ],
  "Luton": [
    "Bedford",
    "Cambridge",
    "London",
    "Milton Keynes",
    "St Albans"
  ],
  "Chelmsford": [
    "London"
  ],
  "Dartford": [
    "London"
  ],
  "Gravesend": [
    "London"
  ],
  "Sevenoaks": [
    "London"
  ],
  "Epsom": [
    "London"
  ],
  "Heathrow Airport": [
    "London"
  ],
  "Stockport": [
    "Manchester"
  ],
  "Salford": [
    "Manchester"
  ],
  "Oldham": [
    "Manchester"
  ],
  "Bolton": [
    "Manchester"
  ],
  "Rochdale": [
    "Manchester"
  ],
  "Bury": [
    "Manchester"
  ],
  "Wigan": [
    "Manchester"
  ],
  "Warrington": [
    "Manchester"
  ],
  "Altrincham": [
    "Manchester"
  ],
  "Macclesfield": [
    "Manchester"
  ],
  "Manchester Airport": [
    "Manchester"
  ],
  "Solihull": [
    "Birmingham"
  ],
  "Sutton Coldfield": [
    "Birmingham"
  ],
  "West Bromwich": [
    "Birmingham"
  ],
  "Dudley": [
    "Birmingham"
  ],
  "Walsall": [
    "Birmingham"
  ],
  "Tamworth": [
    "Birmingham"
  ],
  "Redditch": [
    "Birmingham"
  ],
  "Bromsgrove": [
    "Birmingham"
  ],
  "Birmingham Airport": [
    "Birmingham"
  ],
  "Wakefield": [
    "Leeds"
  ],
  "Huddersfield": [
    "Leeds"
  ],
  "Halifax": [
    "Leeds"
  ],
  "Dewsbury": [
    "Leeds"
  ],
  "Pudsey": [
    "Leeds"
  ],
  "Otley": [
    "Leeds"
  ],
  "Wetherby": [
    "Leeds"
  ],
  "East Kilbride": [
    "Glasgow"
  ],
  "Paisley": [
    "Glasgow"
  ],
  "Hamilton": [
    "Glasgow"
  ],
  "Coatbridge": [
    "Glasgow"
  ],
  "Motherwell": [
    "Glasgow"
  ],
  "Clydebank": [
    "Glasgow"
  ],
  "Dumbarton": [
    "Glasgow"
  ],
  "Glasgow Airport": [
    "Glasgow"
  ],
  "Livingston": [
    "Edinburgh"
  ],
  "Musselburgh": [
    "Edinburgh"
  ],
  "Dalkeith": [
    "Edinburgh"
  ],
  "Dunfermline": [
    "Edinburgh"
  ],
  "Kirkcaldy": [
    "Edinburgh"
  ],
  "Edinburgh Airport": [
    "Edinburgh"
  ],
  "Birkenhead": [
    "Liverpool"
  ],
  "St Helens": [
    "Liverpool"
  ],
  "Southport": [
    "Liverpool"
  ],
  "Bootle": [
    "Liverpool"
  ],
  "Widnes": [
    "Liverpool"
  ],
  "Filton": [
    "Bristol"
  ],
  "Weston-super-Mare": [
    "Bristol"
  ],
  "Portishead": [
    "Bristol"
  ],
  "Clevedon": [
    "Bristol"
  ],
  "Thornbury": [
    "Bristol"
  ],
  "Keynsham": [
    "Bristol"
  ],
  "Bristol Airport": [
    "Bristol"
  ],
  "Belfast": [
    "Derry",
    "Dublin",
    "Edinburgh",
    "Glasgow",
    "Liverpool"
  ],
  "Dublin": [
    "Belfast"
  ],
  "Derry": [
    "Belfast"
  ],
  "Aberdeen": [
    "Dundee",
    "Edinburgh",
    "Glasgow",
    "Inverness",
    "Perth"
  ],
  "Dundee": [
    "Aberdeen",
    "Edinburgh",
    "Glasgow",
    "Perth",
    "St Andrews"
  ],
  "Inverness": [
    "Aberdeen",
    "Edinburgh",
    "Glasgow"
  ],
  "Perth": [
    "Aberdeen",
    "Dundee",
    "Edinburgh",
    "Glasgow"
  ],
  "St Andrews": [
    "Dundee"
  ],
  "Swansea": [
    "Birmingham",
    "Bristol",
    "Cardiff",
    "London"
  ],
  "Milton Keynes": [
    "Birmingham",
    "Cambridge",
    "Leicester",
    "London",
    "Luton",
    "Northampton",
    "Oxford"
  ],
  "Northampton": [
    "Birmingham",
    "Cambridge",
    "Coventry",
    "Leicester",
    "London",
    "Milton Keynes",
    "Oxford"
  ],
  "Coventry": [
    "Birmingham",
    "Leicester",
    "London",
    "Northampton",
    "Nottingham",
    "Warwick",
    "Wolverhampton"
  ],
  "Warwick": [
    "Coventry"
  ],
  "Bradford": [
    "Harrogate",
    "Leeds",
    "Manchester",
    "Sheffield",
    "York"
  ],
  "Harrogate": [
    "Bradford"
  ],
  "Portsmouth": [
    "Bournemouth",
    "Brighton",
    "Chichester",
    "London",
    "Southampton",
    "Winchester"
  ],
  "Chichester": [
    "Portsmouth"
  ],
  "Winchester": [
    "Portsmouth"
  ],
  "Bournemouth": [
    "Portsmouth"
  ],
  "Derby": [
    "Birmingham",
    "Leicester",
    "Manchester",
    "Nottingham",
    "Sheffield",
    "Stoke-on-Trent"
  ],
  "Stoke-on-Trent": [
    "Birmingham",
    "Crewe",
    "Derby",
    "Manchester",
    "Nottingham",
    "Sheffield",
    "Wolverhampton"
  ],
  "Norwich": [
    "Cambridge",
    "Ipswich",
    "Kings Lynn",
    "London",
    "Peterborough"
  ],
  "Ipswich": [
    "Bury St Edmunds",
    "Cambridge",
    "Colchester",
    "London",
    "Norwich"
  ],
  "Peterborough": [
    "Norwich"
  ],
  "Kings Lynn": [
    "Norwich"
  ],
  "Crewe": [
    "Stoke-on-Trent"
  ],
  "Wolverhampton": [
    "Birmingham",
    "Coventry",
    "Manchester",
    "Shrewsbury",
    "Stoke-on-Trent"
  ],
  "Shrewsbury": [
    "Wolverhampton"
  ],
  "Swindon": [
    "Bath",
    "Bristol",
    "London",
    "Oxford",
    "Reading"
  ],
  "Bath": [
    "Swindon"
  ],
  "Colchester": [
    "Ipswich"
  ],
  "Bury St Edmunds": [
    "Ipswich"
  ],
  "Gatwick Airport": [
    "Brighton",
    "London"
  ],
  "Stansted Airport": [
    "Cambridge",
    "London"
  ],
  "Luton Airport": [
    "London"
  ],
  "Liverpool Airport": [
    "Liverpool",
    "Manchester"
  ],
  "Newcastle Airport": [
    "Edinburgh",
    "Newcastle"
  ],
  "Leeds Bradford Airport": [
    "Leeds",
    "Manchester"
  ],
  "Basingstoke": [
    "Reading"
  ],
  "Newbury": [
    "Reading"
  ],
  "Bedford": [
    "Luton"
  ]
};
