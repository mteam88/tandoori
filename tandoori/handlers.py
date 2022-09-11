import tokenize
from io import BytesIO

class Handler:
    def handle(toks, tok):
        pass

class IncrHandler(Handler):
    def handle(self, toks, tok):
        if tok.string == 'incr':
            i = toks.index(tok)
            var = toks[i+1]
            increment = toks[i+2]
            outstr = f"{var.string} += {increment.string}\n"
            ret = list(tokenize.tokenize(BytesIO(outstr.encode('utf-8')).readline))
            return tok.line, ret

HANDLERS = [IncrHandler()]