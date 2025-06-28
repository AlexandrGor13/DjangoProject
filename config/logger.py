import logging


logger = logging.getLogger(__name__)
levels = (logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL)
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-15s %(name)-5s %(levelname)-8s IP: %(ip)-15s User: %(user)-8s %(message)s",
)
