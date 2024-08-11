from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models import CTLBRD01, CTLBRD00
from flask import jsonify

class APIBaseService:
    
    @staticmethod
    def send_response(res, response):
        return res.status(response.get('statusCode', 500)).json(response)

    @staticmethod
    def error_handler(error):
        try:
            error_details = {
                'message': str(error),
                # Add additional fields as needed
            }
            print('Database Error:', error_details)
            return f"Error: {str(error)}"
        except Exception as e:
            print(e)
            return str(e)

    @staticmethod
    def get_control_board_settings(company, whse, inowner, setid):
        try:
            ins_ctlbrd01 = CTLBRD01.query.filter_by(COMPANY=company, WHSE=whse, INOWNER=inowner, SETID=setid).first()
            if not ins_ctlbrd01:
                ins_ctlbrd00 = CTLBRD00.query.filter_by(SETID=setid).first()
                return ins_ctlbrd00.SETTVAL if ins_ctlbrd00 else None
            return ins_ctlbrd01.SETTVAL
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def shelf_life_percentage(company, whse, inowner):
        return APIBaseService.get_control_board_settings(company, whse, inowner, 'SELFLIFEDANGERPERCENTAGE')

    @staticmethod
    def default_mhe_type(company, whse, inowner):
        return APIBaseService.get_control_board_settings(company, whse, inowner, 'DEFAULTMHETYPE')

