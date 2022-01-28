from src import create_app
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = create_app()
