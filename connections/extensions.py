from flask_caching import Cache
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from connections.config import Config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
cors = CORS()
cache = Cache(config={
    'CACHE_TYPE': Config.CACHE_TYPE,
    'CACHE_REDIS_URL': Config.CACHE_REDIS_URL
})
