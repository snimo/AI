import logging
logging.basicConfig(format='%(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

def loguear(mensaje):
    logging.debug("hola a topdps "+ __name__)
