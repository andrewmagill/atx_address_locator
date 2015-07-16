###atx address locator

Python module that returns (through the `locate` function) arcgis server style address matches (including coordinates) for search strings that closely resemble real Austin addresses.

######Example:
```Python
>>> from locator import locate
>>> locate('2201 Barton Springs Rd')
'{"candidates": [{"attributes": {}, "score": 100, "location": {"y": 10069770.259954542,
"x": 3105988.951116815}, "address": "2201 BARTON SPRINGS RD"}], "spatialReference":
{"wkid": 102739, "latestWkid": 2277}}'
```

Address coordinates are returned in the **Central Texas NAD 1983 State Plane** projection, simply because the City of Austin uses this projection in their data.  The address point shapefile can be downlaoded here: [City of Austin GIS Data][atx]

>Todo: Reproject coordinates to user specified spatial reference.  Like so:


```Python
>>> from locator import locate
>>> locate('2201 Barton Springs Rd', wkid=102100)
'{"candidates": [{"attributes": {}, "score": 100, "location": {"y": 3537774.7395377816,
"x": -10883622.235750372}, "address": "2201 BARTON SPRINGS RD"}], "spatialReference":
{"wkid": 102739, "latestWkid": 2277}}'
```

This address locating business is made possible by awesome work done by other people.  I'm reading the data, and executing a SQL query, using the [GDAL][GDAL] geo-spatial library, and parsing the user input into address component parts (address number, street name, etc.) using the [USAddress][USAddress] python module created by [datamade][datamade].  USAddress in turn uses a bunch of other stuff, most notable the awesome [CRFSuite][CRFSuite] NLP library.

######Install:
* create a new virtualenv
* pip install usaddress
* download and install [GDAL with Python bindings][pygdal]
* move GDAL.framework from /Library/Frameworks to your virtualenv sitepackages (e.g. ~/.virtualenvs/mypyenv/lib/python2.7/site-packages)

Haven't tested this with Python 3, but it should work without major modifications.

######Current limitations:
* slow, locate takes about 3 seconds avg on my macbook
* hacking around the fact that USAddress was trained against a different set of addresses, need to train against actual Austin addresses, need to understand CRFSuite a bit to do that.
* does not currently reproject coordinates to different spatial references
* reads data from shapefile, no db support

[USAddress]: https://github.com/datamade/usaddress
[datamade]: http://datamade.us/
[parserator]: https://parserator.datamade.us/usaddress
[GDAL]: http://www.gdal.org/
[pygdal]: https://pypi.python.org/pypi/GDAL/
[atx]: http://goo.gl/M2JIme
[CRFSuite]: http://www.chokkan.org/software/crfsuite/
[pypi-gdal]: https://pypi.python.org/pypi/GDAL/
