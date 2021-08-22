import unittest

from operations.query.test.query_model_constructor_test import QueryModelConstructorTest
from node.test.node_codec_test import NodeCodecTest
from utils.test.query_parser_test import QueryParserTest
from utils.test.typing_parser_test import TypingParserTest

from dotenv import load_dotenv

load_dotenv(dotenv_path='test/.testenv', override=True)


class Test(unittest.TestSuite):
    def test_app(self):
        self.addTests([
            NodeCodecTest(),
            TypingParserTest(),
            QueryParserTest(),
            QueryModelConstructorTest(),
            QueryResolverTest(),
            QueryTest()
        ])

# python -m unittest test.py
