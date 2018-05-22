from app import create_app, db

app = create_app('development')

print("Rerun")

with app.app_context():
    db.create_all()

app.run()
