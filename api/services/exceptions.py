class ExternalServiceError(Exception):
    def __init__(self, error: Exception, detail: str):
        self.error = error
        self.detail = detail
        super().__init__(error)
