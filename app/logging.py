"""
Logging configuration
"""
import json
import logging
import logging.config

import structlog
from flask import request

from app.config import Config


class RequestContext(logging.Filter):
    """ Enhances log messages with contextual information """
    def filter(self, record):
        try:
            record.request = {
                "remote_ip": request.remote_addr,
                "method": request.method,
                "path": request.path,
                "headers": dict(request.headers),
            }
        except RuntimeError:
            pass
        return True


def setup_logging():
    timestamper = structlog.processors.TimeStamper(
        fmt='ISO',
        utc=True,
    )
    pre_chain = [
        structlog.stdlib.add_log_level,
        timestamper,
    ]
    filters = ['request_context']
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'logstash': {
                '()': 'logstash_formatter.LogstashFormatterV1',
            },
            'dev': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(colors=True),
                'foreign_pre_chain': pre_chain,
            }
        },
        'filters': {
            'request_context': {
                '()': RequestContext
            },
        },
        'handlers': {
            'console': {
                'level': Config.LOG_LEVEL,
                'class': 'logging.StreamHandler',
                'formatter': 'dev',
                'filters': filters
            }
        },
        'loggers': {
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
            'werkzeug': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': False
            }
        }
    }
    logging.config.dictConfig(log_config)
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            timestamper,
            structlog.processors.format_exc_info,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
