from decouple import config
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


DB_USER = config('DB_USER')
DB_PASSWORD = config('DB_PASSWORD')
DB_NAME = config('DB_NAME')


DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, future=True)
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


BOT_TOKEN = config('BOT_TOKEN')
FILE = config('FILE')
ADMIN = config('ADMIN')


#  CONSULTING
NOTIFY_CONSULTING = 'Онлайн-консультация по услуге: {}.\nПользователь: {}'
ALERT_CONSULTING_SUCCESS = 'Анастасия получила ваш запрос на онлайн-консультацию, в ближайшее время она с вами свяжется'
