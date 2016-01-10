import requests
import json

import autocomic.exceptions

class GoogleCustomSearch(object):
      
      base_url = 'https://www.googleapis.com/customsearch/v1'
      
      def __init__(self, api_key=None, cx=None):

          self.api_key = api_key
          self.cx = cx
          self.session = requests.Session()
          self.search_url = "%s?key=%s&cx=%s" % ( self.base_url, self.api_key, self.cx)

      def get_image(self, query):
          """"
          Get an image based on the the parameter query text.
          Return a dict with link, content-type and content.
          """

          search_url = "%s&q=%s&searchType=image&imgSize=medium" % (self.search_url, query)
          
          image = self._image_from_search_result(self._get(search_url))
          
          return image

      def _get(self, url):
          response = self.session.get(url, timeout=5)
          
          try:
                response.raise_for_status()
          except requests.exceptions.HTTPError as e:
                print ("HTTP Error: Message in response: %s" % response.text)
                raise

          return response.content
  
      def _image_from_search_result(self, search_result):
            link, mime = self._get_image_info(search_result)
            
            content = self._get(link)

            _image = {}
            _image['link'] = link
            _image['mime'] = mime
            _image['content'] = content

            return _image
            
      def _get_image_info(self, search_result):
          try:
              result = json.loads(search_result.decode("utf-8"))
          except TypeError as e:
              print ("Search result: %s" % search_result)
              raise TypeError(search_result)
          
          try:
              link = result['items'][0]['link']
              fileFormat = result['items'][0]['mime']
          except KeyError as e:
              raise autocomic.exceptions.NoImageFound("No image for this result: %s" 
                                                      % search_result)

          return (link, fileFormat)
