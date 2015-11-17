import requests
import json


class GoogleCustomSearch(object):
      
      base_url = 'https://www.googleapis.com/customsearch/v1'
      
      def __init__(self, api_key=None, cx=None):

	  self.api_key = api_key
          self.cx = cx
          self.session = requests.Session()
          self.search_url = "%s?key=%s&cx=%s" % ( self.base_url, self.api_key, self.cx)

      def get_image(self, query):
          search_url = "%s&q=%s&searchType=image&imgSize=small" % (self.search_url, query)
          
          image = self._image_from_search_result(self._get(search_url))
          
          return image

      def _get(self, url):
          response = self.session.get(url)
          
          try:
                response.raise_for_status()
          except requests.exceptions.HTTPError as e:
                print "HTTP Error: Message in response: %s" % response.content
                raise

          return response.content
  
      def _image_from_search_result(self, search_result):
            link = self._get_image_link(search_result)
            
            return self._get(link)

      def _get_image_link(self, search_result):
          result = json.loads(search_result)

          image = result['items'][0]['link']
          
          return image
