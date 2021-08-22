import unittest

from devtools import debug

from node.node_codec import NodeCodec
from node.node_finder import NodeFinder


class NodeFinderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.original_dict = {
            'fromage': {
                'with': 'other keys and value',
                'node': NodeCodec.encode('fromage', '123'),
                'nested': {
                    'another_node': NodeCodec.encode('camembert', 'penicillium camembertii'),
                    'with': 'other keys and value'
                }
            },
            'something_strange': {
                'with': 'other keys and value',
                'wow': {
                    'that_s very nested right?': {
                        'with': 'other keys and value',
                        'i"m here': NodeCodec.encode('very_nested_cheese', 'Roquefort')
                    },
                    'with': 'other keys and value'
                }
            },
            'with': 'other keys and value',
            'lets': NodeCodec.encode('test', 'more')
        }

        self.node_dict = {
            'fromage.node': (
                'fromage',
                '123',
            ),
            'fromage.nested.another_node': (
                'camembert',
                'penicillium camembertii',
            ),
            'something_strange.wow.that_s very nested right?.i"m here': (
                'very_nested_cheese',
                'Roquefort',
            ),
            'lets': (
                'test',
                'more',
            ),
        }

        self.injection_dict = {
            'fromage.node': 'resolution of fromage/node',
            'fromage.nested.another_node': 'resolution of fromage/nested/another_node',
            'something_strange.wow.that_s very nested right?.i"m here':
                'resolution of something_strange/wow/that_s very nested right?/i"m here',
            'lets': 'resolution of lets',
        }

        self.final_dict = {
            'fromage': {
                'with': 'other keys and value',
                'node': 'resolution of fromage/node',
                'nested': {
                    'another_node': 'resolution of fromage/nested/another_node',
                    'with': 'other keys and value'
                }
            },
            'something_strange': {
                'with': 'other keys and value',
                'wow': {
                    'that_s very nested right?': {
                        'with': 'other keys and value',
                        'i"m here': 'resolution of something_strange/wow/that_s very nested right?/i"m here'
                    },
                    'with': 'other keys and value'
                }
            },
            'with': 'other keys and value',
            'lets': 'resolution of lets'
        }

    def test_find_nodes(self):
        test = NodeFinder.find_nodes(self.original_dict)
        assertion = self.node_dict
        self.assertEqual(test, assertion)

    def test_inject_nodes(self):
        test = NodeFinder.inject_nodes(self.original_dict, self.injection_dict)
        assertion = self.final_dict
        self.assertEqual(test, assertion)

    def test_node_finder(self):
        node_dict = NodeFinder.find_nodes(self.original_dict)
        injection_dict = {
            k: self.injection_dict[k] for k, v in node_dict.items()
        }
        test = NodeFinder.inject_nodes(self.original_dict, injection_dict)
        assertion = self.final_dict
        self.assertEqual(test, assertion)

# python -m unittest node/test/node_finder_test.py