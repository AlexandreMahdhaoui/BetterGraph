import pytest

from better_graph.node.node_codec import NodeCodec as nc


class NodeCodecTest:
    @pytest.fixture
    def fixture(self):
        self.setup()
        yield

    def test_b64_encode(self):
        test = nc._b64_encode(self.decoded)
        assertion = self.encoded
        assert (test == assertion)

    def test_b64_decode(self):
        test = nc._b64_decode(self.encoded)
        assertion = self.decoded
        assert (test == assertion)

    def test_encode(self):
        test = nc.encode(self.node_name, self.object_id)
        assertion = self.encoded_node
        assert (test == assertion)

    def test_decode(self):
        test = nc.decode(self.encoded_node)
        assertion = (self.node_name, self.object_id)
        assert (test == assertion)

    def setup(self) -> None:
        self.decoded = """Let's go over the code snippet above. We open the file using open('my_image.png', 'rb'). Note how we passed the 'rb' argument along with the file path - this tells Python that we are reading a binary file. Without using 'rb', Python would assume we are reading a text file.We then use the read() method to get all the data in the file into the binary_file_data variable. Similar to how we treated strings, we Base64 encoded the bytes with base64.b64encode and then used the decode('utf-8') on base64_encoded_data to get the Base64 encoded data using human-readable characters.Executing the code will produce similar output to:"""
        self.encoded = """TGV0J3MgZ28gb3ZlciB0aGUgY29kZSBzbmlwcGV0IGFib3ZlLiBXZSBvcGVuIHRoZSBmaWxlIHVzaW5nIG9wZW4oJ215X2ltYWdlLnBuZycsICdyYicpLiBOb3RlIGhvdyB3ZSBwYXNzZWQgdGhlICdyYicgYXJndW1lbnQgYWxvbmcgd2l0aCB0aGUgZmlsZSBwYXRoIC0gdGhpcyB0ZWxscyBQeXRob24gdGhhdCB3ZSBhcmUgcmVhZGluZyBhIGJpbmFyeSBmaWxlLiBXaXRob3V0IHVzaW5nICdyYicsIFB5dGhvbiB3b3VsZCBhc3N1bWUgd2UgYXJlIHJlYWRpbmcgYSB0ZXh0IGZpbGUuV2UgdGhlbiB1c2UgdGhlIHJlYWQoKSBtZXRob2QgdG8gZ2V0IGFsbCB0aGUgZGF0YSBpbiB0aGUgZmlsZSBpbnRvIHRoZSBiaW5hcnlfZmlsZV9kYXRhIHZhcmlhYmxlLiBTaW1pbGFyIHRvIGhvdyB3ZSB0cmVhdGVkIHN0cmluZ3MsIHdlIEJhc2U2NCBlbmNvZGVkIHRoZSBieXRlcyB3aXRoIGJhc2U2NC5iNjRlbmNvZGUgYW5kIHRoZW4gdXNlZCB0aGUgZGVjb2RlKCd1dGYtOCcpIG9uIGJhc2U2NF9lbmNvZGVkX2RhdGEgdG8gZ2V0IHRoZSBCYXNlNjQgZW5jb2RlZCBkYXRhIHVzaW5nIGh1bWFuLXJlYWRhYmxlIGNoYXJhY3RlcnMuRXhlY3V0aW5nIHRoZSBjb2RlIHdpbGwgcHJvZHVjZSBzaW1pbGFyIG91dHB1dCB0bzo="""

        self.node_name = 'fromage'
        self.object_id = '507f191e810c19729de860ea'
        self.encoded_node = '__NODE__ZnJvbWFnZTogNTA3ZjE5MWU4MTBjMTk3MjlkZTg2MGVh'

