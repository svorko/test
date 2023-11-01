from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, _app_ctx_stack, jsonify
from sqlalchemy.orm import scoped_session
from sqlalchemy import Column, Integer, String, Float

SQLALCHEMY_DATABASE_URL = "sqlite:///accounting2.sq3"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Accounting(Base):
    __tablename__ = 'accounting'

    id = Column(Integer, primary_key=True)
    cc = Column(String)
    produkt = Column(String)
    menge = Column(Float)

    @property
    def serialize(self):
        """
        Return item in serializeable format
        """
        return {"id": self.id, "cc": self.cc, "product": self.produkt, "amount": self.menge}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Our very hard to guess secretf for the Python study group'
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

@app.route('/items')
def get_accounting():
  accounting_list = app.session.query(Accounting).all()
  return jsonify([item.serialize for item in accounting_list])

@app.teardown_appcontext
def remove_session(*args, **kwargs):
    app.session.remove()

if __name__ == "__main__":
    app.run(host='localhost')