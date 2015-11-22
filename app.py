from flask import Flask, request, render_template
from werkzeug.exceptions import BadRequest

from autocomic import AutoComic, GooglePanelFactory
from autocomic.googlesearch import GoogleCustomSearch

app = Flask("autocomic")
search_engine_id = ''
client_key = ''

@app.route("/autocomicforthepeople/", methods=['GET', 'POST'])
def autocomic():

    if request.method == 'POST':
        autocomic = get_comic()
        validate_input()
        response_payload = render_template("autocomicview.html", 
                                           script = request.form['script'], autocomic = autocomic )
    if request.method == 'GET':
        response_payload = render_template("autocomicview.html")
    
    return response_payload

@app.route("/hello/")
def hello():
    return "Hello World!"

def get_comic():
    
    panel_factory = GooglePanelFactory(
        GoogleCustomSearch(cx=search_engine_id, api_key=client_key)
    )
    autocomic = AutoComic(request.form['script'], panel_factory)
    autocomic.get_good_art()
    
    return autocomic

def validate_input():
    
    if 'script' not in request.form: 
        raise BadRequest(description="Missing value for attribute script.")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

