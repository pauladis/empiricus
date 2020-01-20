from sql_alchemy import _database

class TickerModel(_database.Model):

    __tablename__ = 'ticker'

    ticker_id = _database.Column(_database.Integer, primary_key=True)
    ticker = _database.Column(_database.String(6))
    interrompido = _database.Column(_database.Boolean, default=False)


    def __init__(self, **kwargs):
        self.ticker = kwargs['ticker']
        self.interrompido = kwargs['interrompido']

    def json(self):
        return {
            'ticker_id': self.ticker_id,
            'ticker': self.ticker,
            'interrompido': self.interrompido
        }

    def save(self):
        _database.session.add(self)
        _database.session.commit()

    def delete(self):
        _database.session.delete(self)
        _database.session.commit()

    def update(self):
        self.interrompido = True

    @classmethod
    def findTicker(cls, ticker):
        ticker = cls.query.filter_by(ticker=ticker).first()
        if ticker:
            return ticker
        return False