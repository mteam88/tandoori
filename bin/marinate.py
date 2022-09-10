import tokenize
import copy
from io import BytesIO
import py_compile
import click

FILE_IN = 'tik.tand'
FILE_OUT = FILE_IN.split('.')[0] + ".py"

def stmt_incr(toks, tok):
    i = toks.index(tok)
    var = toks[i+1]
    increment = toks[i+2]
    outstr = f"{var.string} += {increment.string}"
    ret = list(tokenize.tokenize(BytesIO(outstr.encode('utf-8')).readline))
    return ret

@click.command()
@click.argument('FILE_IN')
def marinate(FILE_IN):
    with open(FILE_IN, 'r') as f:
        tokens = list(tokenize.generate_tokens(f.readline))
        out = []
        donelines = []
        for token in tokens:
            toktype, tokval, _, _, tokline = token
            if tokval == "incr":
                for newtoktype, newtokval, _, _, _ in stmt_incr(tokens, token):
                    out.append((newtoktype, newtokval))
                out.append((tokenize.NEWLINE, '\n'))
                donelines.append(tokline)
            elif tokline in donelines:
                pass
            else:
                out.append((toktype, tokval))
    with open(FILE_OUT, 'w') as f:
        f.write(tokenize.untokenize(out).decode('utf-8'))

    exec(open(FILE_OUT).read())
