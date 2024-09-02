import logging


def log_error(message, exception):
    "Logs an error message with exception details."

    logging.error(
        f"{message}: {str(exception)}",
        exc_info=True,
        stack_info=True,
    )
