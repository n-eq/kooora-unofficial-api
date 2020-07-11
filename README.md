# kooora-unofficial-api
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/kooora)](https://pepy.tech/project/kooora)
![Upload Python Package](https://github.com/marrakchino/kooora-unofficial-api/workflows/Upload%20Python%20Package/badge.svg)

[Kooora](kooora.com) unofficial Python API.

## Install
`pip install kooora`

## Usage

Below are some basic examples to use the library:

* Init Kooora class
```python
>>> from kooora import *
>>> api = Kooora()
```

* Fetch today matches
```python
>>> today_matches = api.get_today_matches()
>>> print('Leagues played today:")
>>> for league in today_matches.keys()[:4]:
...     print(league)
(ﺭﻮﻬﻤﺟ ﻥﻭﺪﺑ ﺐﻌﻠﺗ) ﻰﻟﻭﻷﺍ ﺔﺟﺭﺪﻟﺍ ﻲﻧﺎﺒﺳﻹﺍ ﻱﺭﻭﺪﻟﺍ
(ﺭﻮﻬﻤﺟ ﻥﻭﺪﺑ ﺐﻌﻠﺗ) A ﺔﺟﺭﺪﻟﺍ ﻲﻟﺎﻄﻳﻹﺍ ﻱﺭﻭﺪﻟﺍ
(ﺭﻮﻬﻤﺟ ﻥﻭﺪﺑ ﺐﻌﻠﺗ) ﺔﺜﻟﺎﺜﻟﺍ ﺔﺟﺭﺪﻟﺍ ﺔﻴﺑﻮﻨﺠﻟﺍ ﺎﻳﺭﻮﻛ ﻱﺭﻭﺩ
ﺯﺎﺘﻤﻤﻟﺍ ﻱﺪﻨﻠﻨﻔﻟﺍ ﻱﺭﻭﺪﻟﺍ
...
>>> for league in today_matches.keys():
...     print(league)
...     for match in league:
...         print(match)
...
ﻰﻟﻭﻷﺍ ﺔﺟﺭﺪﻟﺍ ﻲﻛﺮﺘﻟﺍ ﻱﺭﻭﺪﻟﺍ
(1710516) 2020-07-11T17:00:00 vs 9323)ﺭﻮﺒﺳ ﺮﻬﻴﺸﻴﻜﺳﺃ (16647)ﺭﻮﺒﺳ ﺮﻴﺴﻴﻜﻴﻟﺎﺑ)
(ﺭﻮﻬﻤﺟ ﻥﻭﺪﺑ ﺐﻌﻠﺗ) ﻰﻟﻭﻷﺍ ﺔﺟﺭﺪﻟﺍ ﻲﻧﺎﺒﺳﻹﺍ ﻱﺭﻭﺪﻟﺍ
(1701509) 2020-07-11T15:00:00 vs 65)ﻮﻐﻴﻓ ﺎﺘﻠﻴﺳ (70)ﺎﻧﻮﺳﺎﺳﻭﺃ)
(1701510) 2020-07-11T17:30:00 vs 63)ﺔﻧﻮﻠﺷﺮﺑ (78)ﺪﻴﻟﻮﻟﺍ ﺪﻠﺑ)
(1701513) 2020-07-11T20:00:00 vs 64)ﺲﻴﺘﻴﺑ ﻝﺎﻳﺭ (62)ﺪﻳﺭﺪﻣ ﻮﻜﻴﺘﻠﺗﺃ)
...
```

* Pick a match and fetch some basic stats
```python
>>> m = api.get_yesterday_matches[17519][0]
>>> stats = m.get_stats()
>>> print(stats['Team1']['Name'])
'ﺪﻴﻟﻮﻟﺍ ﺪﻠﺑ'
>>> print(json.dumps(stats['Team1Stats'], indent=2))
{
  "Tackles": 8,
  "ShirtColor": "#660099",
  "PenaltyKicks": -1,
  "ShotsOnGoal": 4,
  "Interceptions": 11,
  "Saves": 5,
  "Fouls": 15,
  "Catches": 4,
  "Passes": 309,
  "Shots": 13,
  "Assists": -1,
  "ShortColor": "#",
  "Formation": "4-3-1-2",
  "YellowCards": 2,
  "Corners": 4,
  "Possesion": 39,
  "PenaltySaves": -1,
  "Touches": 611,
  "Blocks": 21,
  "Offsides": -1,
  "Crosses": 30,
  "RedCards": -1
}
>>> print(stats['Team2']['Name'])
'ﺔﻧﻮﻠﺷﺮﺑ'
>>> print(json.dumps(stats['Team2Stats'], indent=2))
{
  "Tackles": 14,
  "ShirtColor": "#FFFF00",
  "PenaltyKicks": -1,
  "ShotsOnGoal": 6,
  "Interceptions": 12,
  "Saves": 4,
  "Fouls": 13,
  "Catches": 2,
  "Passes": 626,
  "Shots": 9,
  "Assists": 1,
  "ShortColor": "#",
  "Formation": "4-1-2-1-2",
  "YellowCards": 2,
  "Corners": 5,
  "Possesion": 61,
  "PenaltySaves": -1,
  "Touches": 939,
  "Blocks": 11,
  "Offsides": -1,
  "Crosses": 6,
  "RedCards": -1
}
```

* Init League from ID and fetch ranking and top scorers
```python
>>> liga = League.from_id(17519) # you can also use api.search
>>> liga_table = liga.get_table()
>>> print("%2s %20s %2s %2s %2s %2s" % ("No", "Name", "Pts", "W", "L", "T"))
>>> print("%s" % "_" * 35)
>>> for t in liga_table[:5]:
...     print('%2d %20s %2d %2d %2d %2d' % (t['Rank'], t['Team']['Name'], t['Points'], t['Won'], t['Tied'], t['Lost']))
 No                Name Pts W  L  T
 __________________________________
 1           ريال مدريد 77 23  8  3
 2              برشلونة 73 22  7  5
 3        أتلتيكو مدريد 62 16 14  4
 4              إشبيلية 57 15 12  6
 5              فياريال 54 16  6 12
>>> scorers = liga.get_top_scorers()
>>> print("Top 3 scorers:")
>>> for s in scorers[3:]):
...     print("%s, %d goals" % (s['player'].get_name(), s['goals']))
Top 3 scorers:
ليونيل ميسي, 22 goals
كريم بنزيما, 17 goals
جيرارد مورينو, 16 goals
```

* Find a team by name and get its next match
```python
>>> eibar = None
>>> for t in liga.get_teams():
...     if t.get_name() == "إيبار":
...         eibar = t
...         break
>>> print("Eibar next match: %s" % eibar.next_match())
Eibar next match : (1701493) 2020-07-06T20:00:00 vs إشبيلية(76) إيبار(935)    
```

## Contributing
The project is still at a very early stage.
See https://github.com/marrakchino/kooora-unofficial-api/projects/1 for a list 
of ideas or kindly open an issue to raise a bug or submit a feature request.

## Idea 
I've been fiddling with Kooora's website for years trying to understand
the multiple aspects of the data they provide and had the idea of creating a public
API of it knocking around my head since at least 2017. The initial version of this
unofficial API was made possible by reverse-engineering Kooora's official Android
application both by reversing the code and by sniffing the network requests.

## License

* MIT
