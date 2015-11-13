import sys
import requests
from google import google, images
import googlesearch


class AutoComic(object):
    """
    Contain text story and all the comic elements based on this story
    """
    def __init__(self, script):
        self.script = script
        self.panels = [GooglePanel(text) for text in self.split_script_into_elements()]
        self.search = googlesearch.GoogleSearch(cx="017604795262263300250:cjpxtqbxtv0", key="AIzaSyBUoBTFf-KoF-w0qJOBgzWChP02hSjutJo" )

    def split_script_into_elements(self):
        
        return list(self.script)

    def get_good_art(self):

        for panel in self.panels:
            panel.find_art()

class Panel(object):

    def __init__(self, text):
        self.text = text

    def find_art(self):
        pass

    def serialize(self):
        pass


class GooglePanel(Panel):
    
    def __init__(self, text):
        super(GooglePanel, self).__init__(text)
        
        self.google_options = images.ImageOptions()
        self.google_options.size_category = images.SizeCategory.SMALL
        
    def find_art(self):
        results  = google.search_images(self.text, self.google_options)
        
        self.art = self._get_image(results[0].link)

        print "Image: %s" % self.art

    def _get_image(self, url):
        response = requests.get(url)
        
        response.raise_for_status()

        return response.content

def main():
    
    print("Give me a story:")

    script = []
    for line in sys.stdin:
        script.append(line)

    autocomic = AutoComic(script)
    autocomic.get_good_art()

    print "Number of panels: %s" % len(autocomic.panels)

if __name__ == "__main__":
    main()
