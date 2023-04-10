from backend.database import DataBase


class TaxesService:
    def __init__(self):
        self.database = DataBase()
        pass
    
    def get_taxes_data_by_file(
        self, 
        file,
        user_id: int,
        filename
    ):
        file_response = self.database.get_taxes_data_by_file(
            file,
            user_id, 
            filename
        )
        return file_response


