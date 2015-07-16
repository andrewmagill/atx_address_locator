import unittest
from locator import locate
import json

def json_to_dict(results_as_json):
    try:
        result_dict = json.loads(results_as_json)
        candidates = result_dict['candidates']
        return candidates
    except:
        raise Exception("Invalid response")

def num_results(results):
    if type(results) is str:
        results = json_to_dict(results)
    return len(results)

def top_match(results):
    if type(results) is str:
        results = json_to_dict(results)
    top_match = None
    for candidate in results:
        if top_match == None:
            top_match = candidate
        elif candidate['score'] > top_match['score']:
            top_match = candidate
    if top_match == None:
        raise Exception('No addresses matches')
    else:
        return top_match['address']

class LocatorTests(unittest.TestCase):
    """Tests strange addresses, like half addresses,
    half streets, service roads
    """
    def test_half_address(self):
        test_address = "1124 1/2 S IH 35"
        results = locate(test_address)
        self.assertTrue(num_results(results) > 0)
        self.failUnlessEqual(top_match(results),"1124 1/2 S IH 35 SVRD SB")

    def test_full_address(self):
        test_address = "1124 S IH 35"
        results = locate(test_address)
        self.assertTrue(num_results(results) > 0)
        self.failUnlessEqual(top_match(results),"1124 S IH 35 SVRD SB")

    def test_half_street(self):
        test_address = "3000 14th 1/2 st"
        results = locate(test_address)
        self.assertTrue(num_results(results) > 0)
        self.failUnlessEqual(top_match(results),"3006 E 14TH HALF ST")

    def test_east_half_street(self):
        test_address = "3000 E 14th 1/2 st"
        results = locate(test_address)
        self.assertTrue(num_results(results) > 0)
        self.failUnlessEqual(top_match(results),"3006 E 14TH HALF ST")

    #got some issues to work on

if __name__ == '__main__':
    unittest.main()
