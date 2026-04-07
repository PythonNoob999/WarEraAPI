class APIError(Exception):


    def __init__(self, msg: str, *args):
        super().__init__(*args)
        self.msg = msg
    

    def __str__(self) -> str:
        return f"InvalidAPIResponse \n{self.msg}"


class TransactionTypeNotSupported(Exception):


    def __init__(self, tx_type: str, *args):
        super().__init__(*args)
        self.tx_type = tx_type


    def __str__(self):
        return f"This TransactionType is not supported in current lib version ('{self.tx_type}')"