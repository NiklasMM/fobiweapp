from app import app as application
import app.db
if __name__ == "__main__":
    app.db.setup_db()
    application.run(debug=True)
