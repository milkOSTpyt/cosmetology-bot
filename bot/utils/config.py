from decouple import config


BOT_TOKEN = config('BOT_TOKEN')
ADMIN = config('ADMIN')


#  CONSULTING
NOTIFY_CONSULTING = 'Онлайн-консультация по услуге: {}.\nПользователь: {}'
ALERT_CONSULTING_SUCCESS = 'Анастасия получила ваш запрос на онлайн-консультацию, в ближайшее время она с вами свяжется'
