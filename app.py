"""app.py: Extrac list of titles from an online article."""

__author__      = "Francesco Mosconi"
__copyright__   = "Copyright 2015, Francesco Mosconi"

#works with url = 'http://www.lifehack.org/articles/communication/20-timeless-tips-make-the-most-out-life.html'

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField
from wtforms import SubmitField
from wtforms.validators import Required, Optional, Length, URL

import lxml.html as lx
import re

#Initialize Flask App
app = Flask(__name__)

class UrlInputForm(Form):
    url = URLField('Insert URL:', validators=[URL(), Required(), Length(min=4, max=200)])
    submit = SubmitField('Submit')

@app.route('/',methods=['GET', 'POST'])
def extract():
    urlform   = UrlInputForm(csrf_enabled=False)
    titles_summarized = []

    if urlform.validate_on_submit():
        submitted_data = urlform.data

        url = submitted_data['url']

        t = lx.parse(url)
        al_titles = t.findall(".//h2")
        nbeg = re.compile('[0-9]+')

        for e in al_titles:
            txt = e.text
            if nbeg.match(txt):
                 if(txt not in titles_summarized):
                        titles_summarized.append(txt)

    return render_template('summarizer.html',
                            url_form = urlform, 
                            titles_summarized = titles_summarized)

#Handle Bad Requests
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)