class WordListResp:
    def __init__(self, total_count = 0 , data = [], valid = False, message = ''):
        self.total_count = total_count
        self.data = data
        self.valid = valid
        self.message = message

    def serialize(self):
        return {
            'valid': self.valid,
            'message': self.message,
            'data': self.data,
            'total_count': self.total_count
        }

    

