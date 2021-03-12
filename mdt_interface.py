from app import create_app, db
from config import Config

app = create_app()
with app.app_context():
    db.create_all()
app.run(host=Config.HOST, port=Config.PORT)