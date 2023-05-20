from decouple import config, strtobool


DEBUG = strtobool(config('DEBUG'))

# TG BOT
BOT_TOKEN = config('BOT_TOKEN')
ADMIN = config('ADMIN')

# CONSULTING
NOTIFY_CONSULTING = 'Онлайн-консультация по услуге: {}.\nПользователь: {}'
ALERT_CONSULTING_SUCCESS = 'Анастасия получила ваш запрос на онлайн-консультацию, в ближайшее время она с вами свяжется'

# REDIS
REDIS_HOST = config('REDIS_HOST', default='redis')
