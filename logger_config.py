import logging

def setup_logger():
    log_format = "%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Настроим корневой логгер (самый универсальный способ)
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.propagate = False

    file_handler = logging.FileHandler("py_log.log", mode="w", encoding="utf-8")
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    return root_logger
