import os
DB_DETAILS = {
    'dev': {
        'SOURCE_DB': {
            'DB_TYPE': 'mysql',
            'DB_HOST': '34.70.54.149',
            'DB_NAME': 'retail',
            'DB_USER': os.environ.get('SOURCE_DB_USER'),
            'DB_PASS': os.environ.get('SOURCE_DB_PASS'),

        },
        'TARGET_DB': {
            'DB_TYPE': 'postgres',
            'DB_HOST': '34.70.54.149',
            'DB_NAME': 'retail_dw',
            'DB_USER': os.environ.get('TARGET_DB_USER'),
            'DB_PASS': os.environ.get('TARGET_DB_PASS'),
        }
    }
}
