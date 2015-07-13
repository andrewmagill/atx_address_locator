import sys, re, usaddress, logging
from osgeo import ogr

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class USFields(object):
    AddressNumber             = 'AddressNumber'
    AddressNumberSuffix       = 'AddressNumberSuffix'
    StreetNamePreDirectional  = 'StreetNamePreDirectional'
    StreetNamePreType         = 'StreetNamePreType'
    StreetName                = 'StreetName'
    StreetNamePostDirectional = 'StreetNamePostDirectional'
    StreetNamePostType        = 'StreetNamePostType'

class ATXFields(object):
    address     = 'address'
    address_fr  = 'address_fr'
    prefix_dir  = 'prefix_dir'
    prefix_typ  = 'prefix_typ'
    street_nam  = 'street_nam'
    suffix_dir  = 'suffix_dir'
    street_typ  = 'street_typ'

class Messages(object):
    str_req = "String required"
    list_req = "List required"
    dict_req = "Dictionary required"
    bad_results = "Parser results are not valid"
    bad_string = "Invalid search string"

STREET_ADDRESS = "Street Address"

field_map = {
    USFields.AddressNumber             : ATXFields.address,
    USFields.AddressNumberSuffix       : ATXFields.address_fr,
    USFields.StreetNamePreDirectional  : ATXFields.prefix_dir,
    USFields.StreetNamePreType         : ATXFields.prefix_typ,
    USFields.StreetName                : ATXFields.street_nam,
    USFields.StreetNamePostDirectional : ATXFields.suffix_dir,
    USFields.StreetNamePostType        : ATXFields.street_typ,
}

def _sanitize(user_input):
    """strip unwated characters from user input
    """
    if not type(user_input) is str:
        raise TypeError(Messages.str_req)

    # I'm sure this could be done better
    clean = re.sub(r"[;\(\)\[\]\<\>=:*\%\$\`\?]", "", user_input)
    return clean

def _pre_hack(address_string):
    """find and replace some stuff, hopefully won't be necessary
    after training
    """
    if not type(address_string) is str:
        raise TypeError(Messages.str_req)

    return address_string

def _post_hack(address_parts):
    """put parts in the right place, like street type in
    post-type rather than post-direction field. hopefully
    won't be necessary after training
    """
    #if not type(address_parts) is dict:
    #    raise TypeError("dict required")

    return address_parts

def _translate_to_atx(address_parts):
    """takes usfields tuple and returns atx dict
    """
    if not len(address_parts) == 2:
        raise Exception(Messages.bad_results)

    result_type = address_parts[1]

    if not result_type == STREET_ADDRESS:
        raise Exception(Messages.bad_string)

    ordered_dict = address_parts[0]
    atx_address_parts = {}

    for key, value in ordered_dict.items():
        try:
            atx_field = field_map[key]
            atx_address_parts[atx_field] = value
        except:
            logger.info("No ATX map for USAddress field: %s" % key)

    return atx_address_parts

def _parse(address_string):
    """parses address string into atx address parts,
    returns list
    """
    if not type(address_string) is str:
        raise TypeError(Messages.str_req)

    address_string = _sanitize(address_string)
    address_string = _pre_hack(address_string)
    address_parts = usaddress.tag(address_string)
    address_parts = _translate_to_atx(address_parts)
    address_parts = _post_hack(address_parts)
    return address_parts

def _construct_query(address_parts):
    """constructs sql query from address parts,
    returns string
    """
    if not type(address_parts) is dict:
        raise TypeError(Messages.dict_req)

    clause_list = []

    for key, value in address_parts.items():
        clause_list.append("{} = {}".format(key, value))

    query = "select OGR_GEOM_WKT, * from address_point where "

    if len(clause_list) <= 0:
        raise Exception(Messages.bad_results)

    query += clause_list[0]

    for clause in clause_list[1:]:
        query += " and " + clause

    query += ";"

    return query

def _query_db(query):
    """executes sql query against data in shapefile
    """
    #if not type(query) is str:
    #    raise TypeError("string required")
    pass

def _jsonify(address_candidates):
    """returns json string from list of address candidates
    """
    #if not type(address_candidates) is list:
    #    raise TypeError("list required")
    pass

def locate(address_string):
    """returns json address candidates given address string
    """
    if not type(address_string) is str:
        raise TypeError(Messages.str_req)

    address_parts = _parse(address_string)

    print(address_parts)

    query = _construct_query(address_parts)

    print(query)

    results = _query_db(query)
    return _jsonify(results)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(locate(sys.argv[1]))
    else:
        print(locate("2201 Barton Springs Rd"))

#lst = []
#lambdahash = {}
#lambdahash['mult'] = lambda x, y: y.append(x)
#lambdahash['mult'](1, lst)
#lambdahash['mult'](2, lst)
#lambdahash['mult'](3, lst)
#print lst
