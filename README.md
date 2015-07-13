atx address locator project

uses awesome [USAddress module][USAddress] by [datamade][datamade] to parse address string into
standard US Address fields, then uses open source geo-spatial library,
[GDAL][GDAL], to query atx address shapefile (available [here][atx])

USAddress uses the awesome [CRFSuite][CRFSuite] NLP library

todo: learn how to use CRFSuite to train on atx address data

[USAddress]: https://github.com/datamade/usaddress
[datamade]: http://datamade.us/
[GDAL]: http://www.gdal.org/
[atx]: http://goo.gl/M2JIme
[CRFSuite]: http://www.chokkan.org/software/crfsuite/
