# kooora-unofficial-api
[![License: MIT](https://img.shields.io/badge/License-MIT-red.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/kooora)](https://pepy.tech/project/kooora)

[Kooora](kooora.com) unofficial Python API.

## Install
`pip install kooora`

## Usage

Below are some basic examples to use the library:

```python
>>> from kooora import *
>>> api = Kooora()
>>> # Fetch today matches
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
>>> # Find spanish Liga and fetch rankings and top scorers
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

>>> # Find a team by name and fetch its next match
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
