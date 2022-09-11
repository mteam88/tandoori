import tokenize
import copy
from io import BytesIO
import py_compile
import click
import tandoori as tand

@click.command()
@click.argument('file_in')
@click.pass_context
def tandoori(ctx, file_in):
    ctx.forward(marinate)
    exec(open(file_in.split('.')[0] + ".py").read())

@click.command()
@click.argument('file_in')
def marinate(file_in):
    with open(file_in, 'r') as f:
        tokens = list(tokenize.generate_tokens(f.readline))
        out = []
        donelines = []
        for token in tokens:
            toktype, tokval, _, _, tokline = token
            if not tokline in donelines:
                for handler in tand.HANDLERS:
                    handled, (newdonelines, newtokens) = handler.handle(tokens, token)
                    if newdonelines:
                        donelines.append(newdonelines)
                    if handled:
                        for newtoktype, newtokval, _, _, _ in newtokens:
                            out.append((newtoktype, newtokval))
                        break
            else:
                handled = True
            if handled:
                pass
            else:
                out.append((toktype, tokval))
    with open(file_in.split('.')[0] + ".py", 'w') as f:
        f.write(tokenize.untokenize(out).decode('utf-8'))