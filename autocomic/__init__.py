import sys
import requests
import ConfigParser
import argparse

import googlesearch


class AutoComic(object):
    """
    Contain text story and all the comic elements based on this story
    """
    def __init__(self, script, panel_factory):
        self.script = script
        self.panel_factory = panel_factory
        
        self.panels = [self.panel_factory.create_panel(text) for text in 
                       self.split_script_into_elements()]


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
    
    def __init__(self, text, search):
        super(GooglePanel, self).__init__(text)
        self.search = search
        
    def find_art(self):
        self.art = search.get_image(self.text)

        print "Image: %s" % self.art


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

        return GooglePanel(text, search)


def config_values(config_file):
    """
    Get config values google_engine and client_key from config file.
    Raise exception if config values is missing from config file.
    """

    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    
    return (config.get('googlesearch', 'search_engine_id'), 
            config.get('googlesearch', 'client_key'))


def main():

    parser.add_argument('--config', default='autocomic.ini',
                   help='path to config file in ini format')

    parser.parse_args()
    google_engine, client_key = config_values(config)
    
    print("Give me a story:")

    script = []
    for line in sys.stdin:
        script.append(line)

    search = googlesearch.GoogleSearch(cx=google_engine, key=client_key)
    autocomic = AutoComic(script, search)
    autocomic.get_good_art()

    print "Number of panels: %s" % len(autocomic.panels)

if __name__ == "__main__":
    main()
