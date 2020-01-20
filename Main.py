from flask import Flask
from flask_restful import Api
from resources.Ticker import Ticker, Interrompe, Interrompidos
from resources.Valor import Valor, Valores


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.before_first_request
def init_DB():
    _database.create_all()


api.add_resource(Ticker, '/ticker')
api.add_resource(Interrompe, '/ticker/<string:ticker>')
api.add_resource(Interrompidos, '/interrompidos')
api.add_resource(Valor, '/valor')
api.add_resource(Valores, '/valor/<string:ticker>')

if __name__ == '__main__':
    from sql_alchemy import _database
    _database.init_app(app)
    app.run(debug=True)