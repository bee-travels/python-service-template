from app.errors import example_error

def get_data(context):
    context.start("getData")
    context.stop()
    raise example_error.ExampleException("TODO: Implement me!")


def readiness_check():
    return True
