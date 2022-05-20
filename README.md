# Shoonk

Static link shortener without database written in flask.

## How to use

1. Clone this repo, install dependancies and run.
```bash
git clone 'https://github.com/ekm507/shoonk'
cd shoonk
python3 -m pip install flask
python3 app.py
```
2. On the **first** run, this app will ask you two questions.
   1. First, you need to specify the link address where this app is accessible from. For instance, if this app runs in `https://example.com/` you write that.
   2. Next, it will ask you TCP port number for flask app to run.
3. If you are using a reverse proxy, you may need to configure nginx or other stuff in your server.

## How it works

This application makes an html file for each link with a tag for redirecting. So that any webserver can read these files and even if you remove this application, old links can still work.

## TODO

- [ ] Make better webpage for link (add a copy to clipboard button)
- [ ] Add ability to customize link names for short and long links. (/l and /s)
