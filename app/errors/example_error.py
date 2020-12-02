class ExampleException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.errors = "Example Exception"
        print(self.errors)
