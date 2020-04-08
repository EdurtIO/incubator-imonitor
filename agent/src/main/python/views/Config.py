from flask import jsonify

from common.code import CommonCodes

class ConfigController:

    def get_all_default_config(self):
        return jsonify(CommonCodes().load_config())
