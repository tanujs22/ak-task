from flask import Flask, render_template, jsonify, g
import sys
import tools

app = Flask(__name__)
app.url_map.strict_slashes = False

try:
    app.config.from_object('config')
except Exception as e:
    print 'environment config not found'
    sys.exit(1)

if app.debug is not True:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('flask_error.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    file_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

@app.before_request
def pre():
    g.request_start_time = tools.Toolkit.get_timestamp()
    g.processing_time = lambda: int(g.request_end_time - g.request_start_time)

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status' : 'error', 'message' : "Page found, but we'll not show you"}), 404

@app.errorhandler(405)
def not_found(error):
    return jsonify({'status' : 'error', 'message' : 'wrong HTTP method used'}), 405

@app.errorhandler(500)
def internal_error(exception):
  app.logger.exception(exception)
  return jsonify({'status' : 'error', 'message' : 'Server is smoking hot'}), 500

# register blueprints here
from app.college.controller import college_api



app.register_blueprint(college_api)