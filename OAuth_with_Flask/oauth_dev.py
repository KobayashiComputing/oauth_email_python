import sqlalchemy as sa
import sqlalchemy.orm as so
from sendmail_g import app, db
# from gmail.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db}
