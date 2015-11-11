import sys
import Google-Search-API
#import pyside


class AutoComic(object):
    """
    Contain text story and all the comic elements based on this story
    """
    def __init__(self, script):
        self.script = script
        self.panels = [Panel(text) for text in self.split_script_into_elements()]

    def split_script_into_elements(self):
        
        return list(self.script)

    def press(self):
        for panel in self.panels:
            print "something"


class Panel(object):

    def __init__(self, text):
        self.text = text

    def find_art(self, text):
        pass

    def press(self)
    

def main():
    
    print "Give me a story:"

    script = []
    for line in sys.stdin:
        script.append(line)

    for line in script: print line

    autocomic = AutoComic(script)
    autocomic.press()
    
if __name__ == "__main__":
    main()
