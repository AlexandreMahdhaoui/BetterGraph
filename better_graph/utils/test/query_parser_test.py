import unittest

from better_graph.utils.query_parser import QueryParser as qp


class TestQueryParser:
    def test_parse_operator(self):
        test = {
            'brand__eq': 'tome de savoie',
            'brand__ne': 'camembert',
            'year__gt': 2018,
            'year__h4x0R': 1337
        }
        assertion = {
            'brand': {
                '$eq': 'tome de savoie',
            },
            'year': {
                '$gt': 2018
            }
        }
        assert qp.parse(test, excluded_params=['ne']) == assertion


if __name__ == '__main__':
    # python -m unittest utils/test/query_parser_test.py
    unittest.main()
