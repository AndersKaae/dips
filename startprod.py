from waitress import serve
import startweb
serve(startweb.app, host='0.0.0.0', port=80)
