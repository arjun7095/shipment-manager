import io
from http import client


class FakeSocket:
    def __init__(self, text, fileclass=io.BytesIO):
        if isinstance(text, str):
            text = text.encode("ascii")
        self.text = text
        self.fileclass = fileclass
        self.data = b""

    def sendall(self, data):
        self.data += data

    def makefile(self, mode, bufsize=None):
        if mode != "r" and mode != "rb":
            raise client.UnimplementedFileMode()
        return self.fileclass(self.text)
