import peewee
from database_manager import DatabaseManager
from request_manager import Request
from local_settings import DATABASE
from constants import URL
import logging


# Logging basic configuration
logging.basicConfig(filename="logging's.log")

# Connect to database
database_manager = DatabaseManager(
    database_name=DATABASE['name'],
    user=DATABASE['user'],
    password=DATABASE['password'],
    host=DATABASE['host'],
    port=DATABASE['port'],
)

# All lists of datas
names = list()
populations = list()
areas = list()
ideological_allies = list()
infos = list()


class Nation(peewee.Model):
    name = peewee.CharField(max_length=255, null=False, help_text='Nations Name', verbose_name='Nations Name')
    population = peewee.IntegerField(null=False, help_text='Nations Population', verbose_name='Population')
    area = peewee.CharField(max_length=255, null=False, help_text='Nations Area', verbose_name='Area')
    ideological_allies = peewee.TextField(
        null=False, help_text='Nations Ideological Allies', verbose_name='Ideological Allies'
    )
    info = peewee.TextField(null=False, help_text='Info Of Nation', verbose_name='Info')

    class Meta:
        database = database_manager.db


def scrape_data():
    """This function will scrape data from the URL"""
    request_manager = Request(url=URL)
    # Get all nations names
    name_boxes = request_manager.get_all(
        html_tag='h2',
        tag_id_by='class',
        tag_id='header-with-anchor-widget'
    )
    for name in name_boxes:
        names.append(name.text)

    # Get all nations information
    info_boxes = request_manager.get_all(html_tag='blockquote')
    while True:
        if len(info_boxes) == len(names):
            break
        info_boxes.append(None)

    for info in info_boxes:
        if info is None:
            infos.append('None')
        else:
            infos.append(info.text)

    # Get list of information (population, area and ideological allies
    info_list = request_manager.get_all(html_tag='ul')
    # The first ul is not used so we remove that
    info_list.pop(0)

    for item in info_list:
        list_item = item.find_all('li')
        # Get all nations populations
        population_text = list_item[0].text
        # Remove text parts of text to convert it to integer
        population_text = population_text[12:].replace(',', '')
        populations.append(int(population_text))

        # Get all nations areas
        area_text = list_item[1].text
        # Remove unnecessary parts
        area_text = area_text[5:]
        areas.append(area_text)

        # Get all nations ideological allies
        ideological_allies_text = list_item[2].text
        # Remove unnecessary parts
        ideological_allies_text = ideological_allies_text[20:]
        ideological_allies.append(ideological_allies_text)


if __name__ == '__main__':
    try:
        # Create table of Nation model
        database_manager.create_tables(models=[Nation])
        scrape_data()

        number_of_nations = len(names)
        for nation in range(number_of_nations):
            Nation.create(
                name=names[nation],
                population=populations[nation],
                area=areas[nation],
                ideological_allies=ideological_allies[nation],
                info=infos[nation],
            )

    except ValueError as error:
        print('ValueError:', error)
        logging.error(error)
    except AttributeError as error:
        print('AttributeError:', error)
        logging.error(error)
    except TimeoutError as error:
        print('TimeoutError:', error)
        logging.error(error)
    finally:
        if database_manager.db:
            database_manager.db.close()
            print("Database connection is closed")
