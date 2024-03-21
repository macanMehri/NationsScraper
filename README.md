
# Nations Scraper

Scrape data of USA nations from a website and store data in PosgreSQL database or even asks if you want to save them in a csv file too. Very fast to scrape data.


## Authors

- [@macanMehri](https://www.github.com/macanMehri)


## Deployment

To deploy this project run

```bash
  pip install -r requirements.txt
```
Rename sample_settings.py file to local_settings.py. Put your databse informations in it.

```bash
  DATABASE = {
    'name': 'database name',
    'user': 'database user',
    'password': 'database password',
    'host': 'server host maybe localhost',
    'port': 5432
}
```


## Run Locally

Clone the project

```bash
  git clone https://github.com/macanMehri/NationsScraper.git
```

Go to the project directory

```bash
  cd usa_nations_scraper
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Run the program

```bash
  python main.py
```


## Features

- Ease of use
- User friendly
- Scrape very fast
- Maintaining information in a coherent database
- Ability to save information in csv file if needed

