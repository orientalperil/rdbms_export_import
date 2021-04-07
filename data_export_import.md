https://github.com/orientalperil/rdbms_export_import/blob/master/data_export_import.md

There are 2 data sets one for development and one for production.

The goal is to export data from development and load it into production.

The dumpdata command can output data with primary keys or with natural keys.  The first version cannot be loaded into production because the primary keys will clash.

https://github.com/orientalperil/rdbms_export_import/blob/master/exported_polls_from_development.json

The second version is exported with natural keys meaning that it refers to foreign keys using unique keys not integer primary keys.  It also doesn't have its own primary keys so new ones can be assigned.  This file loads cleanly into the production database.

https://github.com/orientalperil/rdbms_export_import/blob/master/exported_polls_from_development_natural_keys.json

Natural key export works because the ORM models are annotated with the names of fields that uniquely identify related rows through the Model.natural_key() and Manager.get_by_natural_key() methods.

https://github.com/orientalperil/rdbms_export_import/blob/master/polls/models.py#L20

# Set up virtualenv

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Load data into development database

```
DATABASE_URL=sqlite:///development.sqlite3 python manage.py migrate
DATABASE_URL=sqlite:///development.sqlite3 python manage.py loaddata development.json
```

# Load data into production database

```
DATABASE_URL=sqlite:///production.sqlite3 python manage.py migrate
DATABASE_URL=sqlite:///production.sqlite3 python manage.py loaddata production.json
```

# Export data with and without natural keys from development database

```
DATABASE_URL=sqlite:///development.sqlite3 python manage.py dumpdata --indent 4 polls --output exported_polls_from_development.json
DATABASE_URL=sqlite:///development.sqlite3 python manage.py dumpdata --indent 4 --natural-foreign --natural-primary polls --output exported_polls_from_development_natural_keys.json
```

# Load the exported data into production database
```
DATABASE_URL=sqlite:///production.sqlite3 python manage.py loaddata exported_polls_from_development_natural_keys.json
```
