from . import xp
#from . import santander

import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('ibapi')
logger.setLevel(logging.INFO)
logger.addHandler(handler)

all = [xp]
