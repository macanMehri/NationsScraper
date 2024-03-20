import peewee
from database_manager import DatabaseManager
from request_manager import Request
from local_settings import DATABASE


# Connect to database
database_manager = DatabaseManager(
    database_name=DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port'],
)


class Nation(peewee.Model):
    name = peewee.CharField(max_length=255, null=False, help_text='Nations Name', verbose_name='Nations Name')
    population = peewee.IntegerField(null=False, help_text='Nations Population', verbose_name='Population')
    area = peewee.FloatField(null=False, help_text='Nations Area', verbose_name='Area')
    ideological_allies = peewee.TextField(
        null=False, help_text='Nations Ideological Allies', verbose_name='Ideological Allies'
    )
    info = peewee.FloatField(null=False, help_text='Info Of Nation', verbose_name='Info')

    class Meta:
        database = database_manager.db


if __name__ == '__main__':
    try:
        database_manager.create_tables(models=[Nation])
    except ValueError as error:
        print('ValueError:', error)
    finally:
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")
