# -*- coding: utf-8 -*-
import os
import logging
import logging.config
from config import BASE_DIR


# conf_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logger.cfg')
log_dir = BASE_DIR + '/logs'
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

log_path = os.path.join(log_dir, 'crawler.log')
log_path_user = os.path.join(log_dir, 'biliuser.log')
log_path_video = os.path.join(log_dir, 'bilivideo.log')
log_path_db = os.path.join(log_dir, 'db.log')
# 使用fileConfig
#logging.config.fileConfig(conf_name)


#使用dictConfig
myconfig_dict = {
    'version': 1.0,
    'formatters': {
        'detail': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'simple': {
            'format': '%(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'detail'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
        'file_user': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path_user,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
        'file_video': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path_video,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
        'file_db': {
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,
            'backupCount': 10,
            'filename': log_path_db,
            'level': 'INFO',
            'formatter': 'detail',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'crawler': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
        },
        'user': {
            'handlers': ['file_user'],
            'level': 'INFO',
        },
        'video': {
            'handlers': ['file_video'],
            'level': 'INFO',
        },
        'storage': {
            'handlers': ['file_db'],
            'level': 'INFO',
        }
    }
}

logging.config.dictConfig(myconfig_dict)

crawlerlog = logging.getLogger('crawler')
biliuserlog = logging.getLogger('user')
bilivideolog = logging.getLogger('video')
#other = logging.getLogger('root')
storagelog = logging.getLogger('storage')

