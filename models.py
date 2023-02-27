from umongo.frameworks import MotorAsyncIOInstance
from umongo import Document, fields


instance = MotorAsyncIOInstance()


def get_db(db):
    instance.set_db(db)


@instance.register
class Note(Document):
    author_id = fields.IntegerField()
    guild_id = fields.IntegerField()
    name = fields.StrField(unique=True)
    body = fields.StrField()

    class Meta:
        collection_name = 'note'