from logging.config import dictConfig
import logging
import os

from termcolor import colored


log_path = "log/"
# Verifica se o diretorio para armexanar os logs não existe
if not os.path.exists(log_path):
   # então cria o diretorio
   os.makedirs(log_path)


dictConfig({
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": colored("[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s", 'cyan', attrs=['dark']),
            'datefmt' : '%d-%m-%Y %H:%M:%S'
        },
        "detailed": {
            "format": "[%(asctime)s] %(levelname)-4s %(funcName)s() L%(lineno)-4d %(message)s - call_trace=%(pathname)s L%(lineno)-4d",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
        # "email": {
        #     "class": "logging.handlers.SMTPHandler",
        #     "formatter": "default",
        #     "level": "ERROR",
        #     "mailhost": ("smtp.example.com", 587),
        #     "fromaddr": "devops@example.com",
        #     "toaddrs": ["receiver@example.com", "receiver2@example.com"],
        #     "subject": "Error Logs",
        #     "credentials": ("username", "password"),
        # },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "log/myapp.error.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        },
        "detailed_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "detailed",
            "filename": "log/myapp.detailed.log",
            "maxBytes": 10000,
            "backupCount": 10,
            "delay": "True",
        }
    },
    "loggers": {
        "myapp.error": {
            "handlers": ["console", "error_file"],  #, email],
            "level": "INFO",
            "propagate": False,
        }
    },
    "root": {
        "handlers": ["console", "detailed_file"],
        "level": "DEBUG",
    }
})


logger = logging.getLogger(__name__)
