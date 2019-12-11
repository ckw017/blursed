import tokenize_rt
import codecs
import encodings
import io
import math

utf_8 = encodings.search_function('utf-8')

def blurse(inst):
    if type(inst) is int:
        return blursedint(inst)
    if type(inst) is float:
        return blursedfloat(inst)
    if type(inst) is complex:
        return blursedcomplex(inst)
    return inst


def blursedcall(self, *args, **kwargs):
    assert len(args) == 1
    assert len(kwargs) == 0
    return blurse(self*args[0])

def blursefunc(func):
    def inner(*args, **kwargs):
        return blurse(func(*args, **kwargs))
    return inner

def blursedclass(cls):
    for attr_str in dir(cls):
        if attr_str in {'__class__', '__subclasshook__', '__init__'}:
            continue
        attr = getattr(cls, attr_str)
        if(hasattr(attr, '__call__')):
            setattr(cls, attr_str, blursefunc(attr))
    cls.__call__ = blursedcall
    return cls

@blursedclass
class blursedint(int):
    def __getitem__(self, other):
        return other[self]

@blursedclass
class blursedfloat(float):
    def __getitem__(self, other):
        fl = math.floor(self)
        ce = math.ceil(self)
        if fl == ce:
            return other[fl]
        return other[fl] * (1 - (self-fl)) + other[ce] * ((self-fl))

@blursedclass
class blursedcomplex(complex):
    pass

def decode(b, errors='strict'):
    u, length = utf_8.decode(b, errors)
    tokens = tokenize_rt.src_to_tokens(u)
    new_tokens = []
    for token in tokens:
        if token.name == 'NUMBER':
            new_tokens.extend(tokenize_rt.src_to_tokens("blurse({})".format(token.src)))
        else:
            new_tokens.append(token)
    return tokenize_rt.tokens_to_src(new_tokens), length

class StreamReader(utf_8.streamreader, object):
    """decode is deferred to support better error messages"""
    _stream = None
    _decoded = False

    @property
    def stream(self):
        if not self._decoded:
            text, _ = decode(self._stream.read())
            self._stream = io.BytesIO(text.encode('UTF-8'))
            self._decoded = True
        return self._stream

    @stream.setter
    def stream(self, stream):
        self._stream = stream
        self._decoded = False

class IncrementalDecoder(codecs.BufferedIncrementalDecoder):
    def _buffer_decode(self, input, errors, final):  # pragma: no cover
        if final:
            return decode(input, errors)
        else:
            return '', 0
    

codec_map = {
    "blursed": codecs.CodecInfo(
        name="blursed",
        encode=utf_8.encode,
        decode=decode,
        incrementalencoder=utf_8.incrementalencoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=utf_8.streamwriter
    )
}

def register():
    codecs.register(codec_map.get)
    __builtins__['blurse'] = blurse

if __name__ == '__main__':
    print(decode(b'123.123'))
    print(decode(b'123.123 (21 + 15)'))
    print(decode(b'23(123123)(123)'))

