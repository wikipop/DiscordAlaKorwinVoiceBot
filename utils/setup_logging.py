import logging


def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        filename="voice_generator.log",
                        filemode="w",
                        format="[%(asctime)s] %(message)s")
    logging.getLogger().addHandler(logging.StreamHandler())