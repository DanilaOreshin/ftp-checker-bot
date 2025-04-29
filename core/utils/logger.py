import logging

logging.basicConfig(level=logging.ERROR,
                    filename='resources/logs/log.log',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger()
