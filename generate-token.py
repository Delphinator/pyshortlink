from shortlink import db
from shortlink.model import Token

session = db.session()
token = Token.generate()
session.add(token)
session.commit()
print(token.token)
