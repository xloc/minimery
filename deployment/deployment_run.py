from app import create_app

app = create_app('deployment')

app.run()