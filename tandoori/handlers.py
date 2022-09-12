import tokenize
from io import BytesIO

class Handler:
    def handle(self, toks, tok):
        pass

class IncrHandler(Handler):
    def handle(self, toks, tok):
        if tok.string == 'incr' and toks[toks.index(tok)+1].string == ">":
            i = toks.index(tok)
            var = toks[i+1]
            increment = toks[i+2]
            outstr = f"{var.string} += {increment.string}\n"
            ret = list(tokenize.tokenize(BytesIO(outstr.encode('utf-8')).readline))
            return True, (tok.line, ret)
        return False, (None, None)

class IImportHandler(Handler):
    def handle(self, toks, tok):
        if tok.string == 'im' and toks[toks.index(tok)+1].string == ">":
            outstr = "import"
            ret = list(tokenize.tokenize(BytesIO(outstr.encode('utf-8')).readline))
            return True, (False, ret)
        return False, (None, None)

# Uncomment for all handlers (default):
HANDLERS = [h() for h in Handler.__subclasses__()]
# Uncomment for specific handlers
#HANDLERS = [IncrHandler()]