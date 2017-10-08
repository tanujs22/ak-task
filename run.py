from app import app
import config
app.run(host='1.0.3.0', port=config.PORT, debug=config.DEBUG)
