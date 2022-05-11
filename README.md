# shoonk

static link shortener without database written in flask.

## how to use

1. clone this repo, install dependancies and run

```bash
git clone 'https://github.com/ekm507/shoonk'
cd shoonk
python3 -m pip install flask
python3 app.py
```

2. on the **first** run, this app will ask you two questions.

- 1. first, you need to specify the link address where this app is accessible from. for instance, if this app runs in `https://example.com/` you write that.

- 2. next, it will ask you TCP port number for flask app to run.

3. if you are using a reverse proxy, you may need to configure nginx or other stuff in your server.


## TODO

1. make better webpage for link (add a copy to clipboard button)

2. add ability to customize link names for short and long links. (/l and /s)
