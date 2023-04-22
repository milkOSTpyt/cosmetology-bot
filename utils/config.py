from decouple import config


BOT_TOKEN = config('BOT_TOKEN')
FILE = config('FILE')
ADMIN = config('ADMIN')


#  CONSULTING
NOTIFY_CONSULTING = 'Онлайн-консультация по услуге: {}.\nПользователь: @{}'
ALERT_CONSULTING_SUCCESS = 'Администратор получил ваш запрос на онлайн-консультацию, в ближайшее время он с вами свяжется'
ALERT_NOT_USERNAME = 'Администратор не получил ваш запрос на онлайн-консультацию, у вас отсутствует @username'
