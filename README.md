# katerSSG



## philosophy
* easy to use
* no JavaScript, neither on client side nor on server side
* CSS should not affect functionality of the page
* usable on any browser, even links
* easy to scrape
* small in size

## usage
### 1. create config files
Run

```bash
$ cp config.json.example config.json
$ cp update.sh.example update.sh
```

and edit the newly created files config.json and update.json.
You should replace all values marked "changeme" by meaningful values.

### 2. setup virtualenv
```bash
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

### 3. create your first post
It is recommended to drop you ssh public key on the server on which you are
going to publish.
By default, update.sh drops index.html, rss.xml and kater.css in the
hosts html/ directory. You may want to change that.

```bash
$ python3 newpost.py -m "Hello world!" -t firstpost -t yeah
$ bash update.sh
```

## todo
[_] code documentation
[_] feature overview
[_] simplify setup and installation
[x] use figlet to create banners
