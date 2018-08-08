#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import subprocess
import sys
import tempfile
import time


def ellipsis(string, length):
    if not string:
        return ''
    if not isinstance(string, str):
        string = str(string)
    if len(string) <= length:
        return string
    if length <= 3:
        return string[:length-1] + '…'
    return string[:length-3] + '...'


def shorten_url(url):
    shortened = ''
    tokens = url.split('/')
    if tokens[0] in ('http:', 'https:'):
        shortened = tokens[2]
    else:
        shortened = tokens[0]
    shortened += '/…/' + tokens[-1]
    return shortened


def title_from_url(url):
    title = shorten_url(url)
    return ellipsis(title, 80)


def create_post(message, tags, urls, config):
    content = ''
    if message:
        content = message
    if not content:
        editor = config.get('editor', '')
        if not editor:
            editor = os.environ.get('EDITOR', 'vim')
        with tempfile.NamedTemporaryFile(suffix='.tmp') as f:
            f.flush()
            subprocess.call([editor, f.name])
            f.seek(0)
            content = f.read().decode('utf-8')
        if not content and not urls:
            return
    if content:
        title = ellipsis(content.splitlines()[0], 80)
    elif urls:
        title = '{}'.format(title_from_url(urls[0]))
    if title == content.strip():
        content = ''
    else:
        content += '<br><br>'
    for i in range(len(urls)):
        url = urls[i]
        line = '[{}] <a href="{}">{}</a><br>\n'.format(i, url, ellipsis(url, 80))
        content += line
    today = datetime.datetime.today()
    h_offset = time.localtime().tm_hour - time.gmtime().tm_hour
    timezone = '%02d00' % h_offset
    if h_offset >= 0:
        timezone = '+' + timezone
    post = {
        'title': title,
        'content': content,
        'tags': tags,
        'pubDate': today.strftime('%a, %d %b %Y %H:%M:%S ') + timezone,
        'link': today.strftime('%Y-%m-%d_%H-%M-%S')
    }
    filename = today.strftime('%Y-%m-%d_%H-%M-%S.json')
    with open('kater/posts/' + filename, 'w') as f:
        json.dump(post, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--tag',
        action='append'
    )
    parser.add_argument(
        '-m',
        '--message'
    )
    parser.add_argument(
        'URL',
        nargs='*'
    )
    args = parser.parse_args()
    tags = args.tag
    message = args.message
    urls = args.URL
    with open('config.json', 'r') as f:
        config = json.load(f)
    create_post(message, tags, urls, config)


if __name__ == '__main__':
    main()
