from flask_restful import Resource, reqparse
from Models.TickerModel import TickerModel
from Models.ValorModel import ValorModel

class Ticker(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('ticker', type=str, required=True, help="o nome do ticker nao pode ser vazio")
    argumentos.add_argument('interrompido', type=bool, default=False)

    def get(self):
        return {'tickers': [t.json() for t in TickerModel.query.all()]}, 200

    def post(self):
        dados = self.argumentos.parse_args()
        if TickerModel.findTicker(dados["ticker"]):
            return {'message': 'Ticker com este nome já existe'}, 401

        ticker = TickerModel(**dados)
        try:
            ticker.save()
        except Exception as e:
            return {'message': e}, 500
        return ticker.json(), 201

class Interrompe(Resource):

    def put(self, ticker):
        ticker = TickerModel.findTicker(ticker)
        if ticker:
            ticker.update()
            try:
                ticker.save()
                resposta = {'message': 'TICKER interrompido'}
                resposta.update(ticker.json())
                return resposta, 200
            except Exception as e:
                return {'message': e}, 500
        return {'message': 'ticker inexistente'}, 404

class Interrompidos(Resource):
    def get(self):
        tickers = []
        [tickers.append(t.json()) for t in TickerModel.query.filter_by(interrompido=True)]
        for t in tickers:
            last_valor = ValorModel.query.filter_by(ticker_id=t['ticker_id']).order_by(ValorModel.valor_id.desc()).first()
            if last_valor is not None:
                t.update({'ultimo valor': last_valor.valor})
        return {'Ticker:': [t for t in tickers]}, 200


