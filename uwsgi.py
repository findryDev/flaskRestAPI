from app import app as application
import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT'))
    application.run(host='0.0.0.0', port=port)
   