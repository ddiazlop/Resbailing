from kivy import Logger


def log_error(error, *args):
    Logger.error('ResbailingError: ' + str(error))
    if args:
        Logger.error('ResbailingErrorData: ' + str(args))

def log_warning(message):
    Logger.warning('ResbailingWarning: ' + message)
