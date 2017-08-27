from flask import Flask
import controllers

app = Flask(__name__, template_folder="templates")

app.register_blueprint(controllers.main)
app.register_blueprint(controllers.about)

if __name__ == '__main__':
    app.run(debug=True)
