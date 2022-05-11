from flask import Flask, request
from sys import argv
import re
import os
from configparser import ConfigParser

def first_run():
    # this function is for making configurations on the first run.


    #Get the configparser object
    config_object = ConfigParser()

    if os.path.exists('configuration'):
        config_object.read('configuration')
        hostname = config_object['APP']['hostname']
        listening_port = config_object['APP']['listening_port']
        last_number = config_object['APP']['last_number']

    else:
        hostname = input("insert hostname which is in form of a link.(eg. https://example.com/ ): ")

        listening_port = int(input("insert listening TCP port for flask (eg. 5000 ): "))

        os.makedirs('l', exist_ok=True)
        existing_links = os.listdir('./l')
        try:
            existing_links = list(filter(lambda x:re.match(r'[0-9]{4}\.html', x), existing_links))
            existing_links.sort()
            last_number = int(existing_links[-1][:4])
        except:
            last_number = 0

        config_object['APP'] = {
            'hostname': hostname,
            'listening_port': listening_port,
            'last_number': last_number,
        }
        with open('configuration', 'w') as conf:
            config_object.write(conf)

        open('last_number', 'w').write(str(last_number))


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
    first_run()
    app.run()