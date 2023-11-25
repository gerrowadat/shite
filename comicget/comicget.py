#!/usr/bin/env python

import logging
import requests
from bs4 import BeautifulSoup
from PIL import Image


class WebComicRequestError(Exception):
    pass


class WebComic(object):
    def __init__(self, name, url):
        self._name = name
        self._url = url
        self._comic_img_url = None

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def comic_img_url(self):
        """Return the URL of the largest image (by area) on the page."""
        if self._comic_img_url:
            return self._comic_img_url
        all_img = self._all_image_urls()
        largest_img = None
        largest_area = 0
        for i in all_img:
            i_area = self._image_area(i)
            if i_area > largest_area:
                largest_area = i_area
                largest_img = i
        self._comic_img_url = largest_img
        return self._comic_img_url

    def _all_image_urls(self):
        """A set of all <img> tag targets."""
        ret = set()
        r = requests.get(self.url)
        if r.status_code != 200:
            raise WebComicRequestError("Error %s getting %s" % (r.status_code, self.url))
        s = BeautifulSoup(r.text, "html.parser")
        for i in s.find_all("img"):
            src = i.get("src")
            if src.startswith("http"):
                ret.add(src)
            elif src.startswith("/"):
                ret.add(self.url.rstrip("/") + src)
            else:
                ret.add(self.url.rstrip("/") + "/" + src)
        return ret

    def _image_area(self, img_url):
        """The area in pixels of a given image."""
        r = requests.get(img_url, stream=True)
        if r.status_code != 200:
            raise WebComicRequestError("Error %s getting %s" % (r.status_code, self.url))
        content_type = r.headers.get("Content-type", None) or r.headers.get("Content-Type", None)
        if not content_type:
            logging.info("%s unknown type (no Content-Type header)" % (img_url))
            for h in r.headers:
                logging.info(" - %s: %s" % (h, r.headers[h]))
            return 0
        if not content_type.startswith("image"):
            logging.info("%s is not an image (%s)" % (img_url, r.headers["Content-type"]))
            return 0
        try:
            i = Image.open(r.raw)
        except Exception as e:
            logging.info("Error analysing %s: %s" % (img_url, str(e)))
            return 0

        return i.size[0] * i.size[1]








