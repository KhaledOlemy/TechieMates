import os
from .engine.file_storage import FileStorage
from .engine.db_storage import DBStorage

# if os.getenv("TM_TYPE_STORAGE") == "db":
#     storage = DBStorage()
# else:
#     storage = FileStorage()

# storage.reload()

storage = DBStorage()

storage.reload()
