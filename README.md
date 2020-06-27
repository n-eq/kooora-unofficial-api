# kooora-unofficial-api
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[Kooora](kooora.com) unofficial Python API.

## Idea 
I've been fiddling with Kooora's website for years trying to understand
the multiple aspects of the data they provide and had the idea of creating a public
API of it knocking around my head since at least 2017. The initial version of this
unofficial API was made possible by reverse-engineering Kooora's official Android
application both by reversing the code and by sniffing the network requests.

## Install
TODO

## Usage

Below are some basic examples to use the library:

```python
>>> from kooora import *
>>> api = Kooora()
>>> kacm_b = api.search_team("أمل الكوكب المراكشي")[0]
>>> print(kacm_b)
Team {name: "أمل الكوكب المراكشي", id: 12551, Sport { (0), has teams: yes}}
>>> # First find the team where Bounou plays in Liga teams, then fetch the next match.
>>> bounou = api.search_player("ياسين بونو")[0]
>>> 
>>> liga = League.from_id(17519)
>>> liga_teams = liga.get_teams()
>>> for team in liga_teams:
>>>     found = False
>>>     team_ext = Team.from_id(team.id)
>>>     for player in team_ext.get_players():
>>>         if player.get_id() == bounou.get_id():
>>>             print("Bounou plays for %s" % team_ext.name)
>>>             print("Bounou next match: %s" % team_ext.next_match())
>>>             found = True
>>>             break
>>>     if found:
>>>         break
Bounou plays for إشبيلية
Bounou next match: (1701486) 2020-06-30T17:30:00 - Team {name: "ليجانيس", id: 940, Sport { (0), has teams: yes}} Team {name: "إشبيلية", id: 76, Sport { (0), has teams: yes}}
``` 

## Contributing
The project is still at a very early stage.
See https://github.com/marrakchino/kooora-unofficial-api/projects/1 for a list 
of ideas or kindly open an issue to raise a bug or submit a feature request.

## License

* MIT
