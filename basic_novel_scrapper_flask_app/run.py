from app import create_app, db
from app.database import init_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db(app)
    app.run(debug=True)