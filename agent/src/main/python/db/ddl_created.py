from Application import db

from common.Code import CommonCodes

db.create_all()

messages = CommonCodes().load_config()

print messages
