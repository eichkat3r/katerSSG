#!/usr/bin/env python3
import json
import os

from jinja2 import Environment, PackageLoader, select_autoescape

from pyfiglet import Figlet


class Post:
    def __init__(self, title, content, tags, pubDate, link):
        self._title = title
        self._content = content
        self._tags = tags
        if tags is None:
            self._tags = []
        self._pubDate = pubDate
        self._link = link

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        return self._content

    @property
    def tags(self):
        return self._tags

    @property
    def pubDate(self):
        return self._pubDate

    @property
    def link(self):
        return self._link


def load_posts(directory):
    posts = []
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            with open(directory + '/' + filename, 'r') as f:
                postdict = json.load(f)
                title = postdict.get('title', '')
                content = postdict.get('content', '')
                tags = postdict.get('tags', [])
                pubDate = postdict.get('pubDate', '')
                link = postdict.get('link', '')
                post = Post(title, content, tags, pubDate, link)
                posts.append(post)
    posts = sorted(posts, key=lambda p: p.link)[::-1]
    return posts


def main():
    with open('config.json', 'r') as f:
        config = json.load(f)
    env = Environment(
        loader=PackageLoader('kater', 'templates'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    base = env.get_template('base.html')
    rss = env.get_template('rssconf.xml')
    posts = load_posts('kater/posts')
    fig = Figlet(font=config.get('font', 'banner'))
    bannertext = config.get('banner', '')
    banner = fig.renderText(bannertext).replace('#', '@')
    with open('index.html', 'w') as f:
        text = base.render(posts=posts, config=config, banner=banner)
        f.write(text)
    with open('rss.xml', 'wb') as f:
        text = rss.render(posts=posts, config=config)
        f.write(text.encode('ascii', 'xmlcharrefreplace'))


if __name__ == '__main__':
    main()
