from flask import Flask, request
from sys import argv
import re


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route("/l/<path:link>")
def shorten(link):
    print(request.host_url)
    last_number = int(open('last_number').read()) + 1
    open('last_number', 'w').write(str(last_number))
    text = f"""
    <!DOCTYPE html>
        <head>
            <meta http-equiv="refresh" content="0; url={link}" />
        </head>
    """
    with open(f'l/{last_number:04d}.html', 'w') as w:
        w.write(text)

    full_link = f"{request.host_url}s/{last_number:04d}.html"

    return f"<a href={full_link}>{full_link}</a>"


@app.route("/s/<link>")
def get_full(link):
    print(link)
    link = link[:4]
    if re.match(r'^[0-9]{4}$', link):
        try:
            return (open(f'l/{link}.html').read())
        except FileNotFoundError:
            return (open(f'404.html').read())
    else:
        return (open(f'404.html').read())


if __name__ == '__main__':
    app.run()