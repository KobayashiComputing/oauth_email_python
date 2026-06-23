from flask import Flask, render_template

# begin - imports for oauth 
from authlib.integrations.flask_client import OAuth
# end - imports for oauth

app = Flask(__name__)

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<\
!\xd5\xa2\xa0\x9fR"\xa1\xa8'

'''
    Set SERVER_NAME to localhost as twitter callback
    url does not accept 127.0.0.1
    Tip : set callback origin(site) for facebook and twitter
    as http://domain.com/ (or use your domain name) as this provider
    don't accept 127.0.0.1 / localhost
'''

app.config['SERVER_NAME'] = 'localhost:5000'

# begin - initialize oauth
oauth = OAuth(app)
# end - initialize oauth


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)