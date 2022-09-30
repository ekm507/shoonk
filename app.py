from flask import Flask
import re
import os
from configparser import ConfigParser

# read from configuration file or set configuration file for first run.
# this function will read hostname and listening_port from config file.
# also it will create last_number file if it does not exist
def first_run():
    # this function is for making configurations on the first run.

    # make ./l directory for storing link files
    os.makedirs('l', exist_ok=True)
    last_number = 0


    global hostname, listening_port

    #Get the configparser object
    config_object = ConfigParser()

    # read configuration from file, if it exists
    if os.path.exists('configuration'):
        config_object.read('configuration')
        hostname = config_object['APP']['hostname']
        listening_port = config_object['APP']['listening_port']

    # generate configuration file if it does not exist
    else:
        hostname = input("insert hostname which is in form of a link.(eg. https://example.com/ ): ")

        listening_port = int(input("insert listening TCP port for flask (eg. 5000 ): "))

        existing_links = os.listdir('./l')
        try:
            existing_links = list(filter(lambda x:re.match(r'[0-9]{4}\.html', x), existing_links))
            existing_links.sort()
            last_number = int(existing_links[-1][:4])
        except:
            last_number = int(0)

        config_object['APP'] = {
            'hostname': hostname,
            'listening_port': listening_port,
        }
        with open('configuration', 'w') as conf:
            config_object.write(conf)

    if not os.path.exists('last_number'):
        open('last_number', 'w').write(str(last_number))


# make a flask app
app = Flask(__name__)
app.url_map.strict_slashes = False

# give it a long link to shorten (/l stands for long link)
@app.route("/l/<path:link>")
def shorten(link):

    # get number of latest link generated so that files will not be overwritten
    last_number = int(open('last_number').read()) + 1

    global hostname

    # if links does not start with "http", add it to the link.
    # this must be done in a way that it supports other protocols too. TODO
    open('last_number', 'w').write(str(last_number))
    if re.match(r'^https:/[^/]', link):
        link = 'https://' + link[7:]
    if link[:4] != 'http':
        link = 'http://' + link
    
    # generate file with redirect tag
    text = f"""
    <!DOCTYPE html>
        <head>
            <meta http-equiv="refresh" content="0; url={link}" />
        </head>
    """
    with open(f'l/{last_number:04d}.html', 'w') as w:
        w.write(text)

    # return link to the file with short link.
    # add ability to change the link. TODO
    full_link = f"{hostname}s/{last_number:04d}.html"

    return f"<a href={full_link}>{full_link}</a>"


# give it a shortened link and it will return the link file.
@app.route("/s/<link>")
def get_full(link):

    # get number of given link
    # if there is any errors, it will return a 404 page
    link = link[:4]
    if re.match(r'^[0-9]{1,4}$', link):
        # if link is not in the directory, return 404
        if not os.path.exists(f'l/{int(link):04d}.html'):
            return (open(f'404.html').read())
        else:
            return (open(f'l/{int(link):04d}.html').read())
    else:
        return (open(f'404.html').read())


# run the application. it will first load/save configuration and then run flask app
if __name__ == '__main__':
    first_run()
    global listening_port
    app.run(port = listening_port)