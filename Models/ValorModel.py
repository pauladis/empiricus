from sql_alchemy import _database
from datetime import datetime

class ValorModel(_database.Model):

    __tablename__ = 'valores'

    now = datetime.now().strftime("%d/%m/%Y")

    valor_id = _database.Column(_database.Integer, primary_key=True)
    ticker_id = _database.Column(_database.Integer, _database.ForeignKey('ticker.ticker_id'))
    valor = _database.Column(_database.Float(precision=2))
    dt_negociacao = _database.Column(_database.DateTime(timezone=True), default=now)

    def __init__(self, ticker_id, **dados):
        self.ticker_id = ticker_id
        self.valor = dados['valor']
        self.dt_negociacao = datetime.now()

    def json(self):
        return {
            'ticker_id': self.ticker_id,
            'valor': self.valor,
            'dt_negociacao': self.dt_negociacao.strftime("%d/%m/%Y")
        }

    def save(self):
        _database.session.add(self)
        _database.session.commit()

    @classmethod
    def find_by_id(cls, id):
        valor = cls.query.filter_by(valor_id=id).first()
        if valor:
            return valor
        return False


