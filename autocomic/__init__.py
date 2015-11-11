import sys
import Google-Search-API
#import pyside


class AutoComic(object):
    """
    Contain text story and all the comic elements based on this story
    """
    def __init__(self, script):
        self.script = script

    def split_script_into_elements(self):
        pass

    def press(self):
        pass


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
    autocomic.draw()
    
if __name__ == "__main__":
    main()
