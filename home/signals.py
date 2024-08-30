from django.db.backends.signals import connection_created
import logging

logger = logging.getLogger(__name__)

def log_queries(sender, connection, **kwargs):
    logger.info(f"Connected to database with {connection.vendor}")

connection_created.connect(log_queries)
