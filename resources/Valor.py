from flask_restful import Resource, reqparse
from Models.ValorModel import ValorModel
from Models.TickerModel import TickerModel

class Valor(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('ticker', type=str, required=True, help="ticker invalido")
    argumentos.add_argument('valor', type=float, required=True, help="é necessario possuir um valor valido")
    #argumentos.add_argument('dt_negociacao', type=lambda x: datetime.strptime(x, '%m/%d/%Y'))

    def get(self):
        return {'valores': [v.json() for v in ValorModel.query.all()]}, 200

    def post(self):
        dados = self.argumentos.parse_args()
        ticker = TickerModel.findTicker(dados['ticker'])
        if ticker:
            if ticker.interrompido is False:
                valor = ValorModel(ticker.ticker_id, **dados)
                try:
                    valor.save()
                    return {'negociacao': valor.json()}, 201
                except Exception as e:
                    return {'message': e}, 500
            return {'message': 'Ticker com negociação interrompida'}, 401
        return {'message': 'Ticker inexistente, favor verificar'}, 404

class Valores(Resource):

    def get(self, ticker):
        valores = []
        ticker = TickerModel.findTicker(ticker)
        media = 0
        cont = 0
        for v in ValorModel.query.filter_by(ticker_id=ticker.ticker_id).order_by\
                    (ValorModel.valor_id.desc()).limit(20):
            media += v.valor
            valores.append(v)
            cont += 1
        total = 20
        if cont < 20:
            total = cont
        return {'media': round(media/total,2) , 'valores': [v.json() for v in valores]}, 200