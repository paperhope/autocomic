import sys
import requests
import configparser
import argparse
import base64
import copy
import PIL
import autocomic.exceptions

from autocomic.googlesearch import GoogleCustomSearch


class AutoComic(object):
    """
    Contain text story and all the comic elements based on this story
    """
    def __init__(self, script, panel_factory,  title="Autocomic for the people"):
        self.script = self._strip_list(script)
        self._panel_factory = panel_factory
        self.title = title

    def initialize_panels(self):

        self.panels = []
        for panel_text in self.script:
            try:
                self.panels.append(self._panel_factory.create_panel(panel_text))
            except autocomic.exceptions.PanelCreationException as e:
                self.panels.append(autocomic.EmptyPanel("No art for you: %s" % panel_text))

    def _strip_list(self, list):

        return [s.strip() for s in list if not s.isspace()]

    def set_panels_art(self):

        try:
            self.panels
        except:
            raise autocomic.exceptions.PanelsNotInitialized()

        for panel in self.panels:
            try:
                panel.find_art()
            except autocomic.exceptions.PanelArtFailed as e:
                panel = autocomic.EmptyPanel(panel.text)

class Panel(object):
    """
    Base Panel class which was have to be subclassed.
    Method find_art must be implmented in each subclass.
    """
    def __init__(self, text):
        self.text = text
        self.art = None
        
    def find_art(self):
        pass

    def serialize(self):
        """
        A panel object is serialized by encoding the binary image in base64, and
        return link, mime and text string unchanged. What? What? encode strings in utf-8?
        """
        serialized_art  = copy.deepcopy(self.art)
        if 'content' in serialized_art:
            serialized_art['content'] = base64.b64encode(serialized_art['content'])

        return (self.text, serialized_art)


class EmptyPanel(object):
    """
    Panel with no art. Just an image with panel text on it.
    """
    def __init__(self, text):
        self.text = text
        self.art = None

    def find_art(self):
        """
        Generate empty image with panel text on it.
        """
        self.art = self._create_text_image()

    def _create_text_image(self):
        img = PIL.Image('RGBA', '', (255,255, 255,0))

        fnt  = PIL.ImageFont.truetype('pillow/Tests/fonts/FreeMono.ttf', 40)
        draw_cntx = PIL.ImageDraw.Draw(img)
        draw_cntx.text((10,10), self.text, font  = fnt, fill=(255, 255, 255, 128))

        return list(img.getdata())

class GooglePanel(Panel):
    
    def __init__(self, text, search):
        super(GooglePanel, self).__init__(text)
        self.search = search
        
    def find_art(self):
        try:
            self.art = self.search.get_image(self.text)
        except Exception as e:
            raise autocomic.exceptions.PanelArtFailed("Could not find art for GooglePanel instance with text: %s" % self.text)

class PanelFactory(object):

    def create_panel(self, text):
        """
        Method MUST be implemented in subclass. 
        Receive text as argument and return a panel instance.
        """
        raise NotImplementedError


class GooglePanelFactory(object):
    """
    Factory class for creating panels with images from google search.
    """
    def __init__(self, search):

        self.search = search

    def create_panel(self, text):

        return GooglePanel(text, self.search)


def config_values(config_file):
    """
    Get config values google_engine and client_key from config file.
    Raise exception if config values is missing from config file.
    """

    config = configparser.SafeConfigParser()
    config.read(config_file)
    
    return (config.get('googlesearch', 'search_engine_id'), 
            config.get('googlesearch', 'client_key'))


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default='autocomic.ini',
                   help='path to config file in ini format')

    args = parser.parse_args()
    search_engine_id, client_key = config_values(args.config)
    
    print("Give me a story:")

    script = []
    for line in sys.stdin:
        script.append(line)

    search = GoogleCustomSearch(cx=search_engine_id, api_key=client_key)
    googlepanel_factory = GooglePanelFactory(search)

    autocomic = AutoComic(script, googlepanel_factory)
    autocomic.create_panels()
    autocomic.get_good_art()


if __name__ == "__main__":
    main()
