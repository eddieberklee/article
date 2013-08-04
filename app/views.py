# Create your views here.

import urllib2
from urlparse import urlparse
from bs4 import BeautifulSoup

from django.http import HttpResponse
from django.shortcuts import render

from app.models import *

def index(request):
    template_name = 'index.html'
    context = {
    }
    return render(request, template_name, context)

import StringIO
import struct

# Code from https://code.google.com/p/bfg-pages/source/browse/trunk/pages/getimageinfo.py
# Adapted per advice from http://stackoverflow.com/questions/7460218/get-image-size-wihout-downloading-it-in-python#comment9025608_7460263
def getImageInfo(url):
    data = urllib2.urlopen(url).read(24)
    data = str(data)
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith('\377\330'):
        content_type = 'image/jpeg'
        # jpeg = StringIO.StringIO(data)
        # jpeg's require more then the .read(24) so we're fetching the whole image
        jpeg = urllib2.urlopen(url)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height

def sanitize_url(url):
    if img_url.startswith('/'):
        img_url = ''.join([urlparse(url).netloc, img_url])
        print img_url
    elif not img_url.startswith('http'):
        img_url = ''.join(['http://',img_url])
    elif urlparse(img_url).netloc == urlparse(url).netloc:
        pass
    elif img_url.startswith(urlparse(url).netloc):
        pass
    return img_url

def url_for_pictures(url):
    pictures = {}
    data = urllib2.urlopen(url).read()
    soup = BeautifulSoup(data)
    imgs = soup.find_all('img')
    for img in imgs:
        if 'width' in img.attrs.keys():
            if img['width'] == '1':
                continue
        if 'height' in img.attrs.keys():
            if img['height'] == '1':
                continue

        img_url = img['src']
        img_url = sanitize_url(img_url)
        img_sizet = getImageInfo(img_url)

        if img_sizet[0] and img_sizet[1] != 1 and img_sizet[2] != 1:
            pictures[img_url] = img_sizet
    return pictures

def add_article(request):
    template_name = 'add_article.html'
    if request.method == 'POST':
        post_data = request.POST

        article_url = post_data['article_link']
        # data = urllib2.urlopen(article_url).read()
        print 'URL',post_data['article_link']

        # pics = url_for_pictures(article_url)

    context = {
        'article_url' : article_url,
        # 'pic_urls': pics.keys()
    }
    return render(request, template_name, context)

