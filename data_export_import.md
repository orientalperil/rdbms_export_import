virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# load data into development database
DATABASE_URL=sqlite:///development.sqlite3 python manage.py migrate
DATABASE_URL=sqlite:///development.sqlite3 python manage.py loaddata development.json

# load data into production database
DATABASE_URL=sqlite:///production.sqlite3 python manage.py migrate
DATABASE_URL=sqlite:///production.sqlite3 python manage.py loaddata production.json

# export data with and without natural keys from development database
DATABASE_URL=sqlite:///development.sqlite3 python manage.py dumpdata --indent 4 polls --output exported_polls_from_development.json
DATABASE_URL=sqlite:///development.sqlite3 python manage.py dumpdata --indent 4 --natural-foreign --natural-primary polls --output exported_polls_from_development_natural_keys.json

# load the exported data into production database
DATABASE_URL=sqlite:///production.sqlite3 python manage.py loaddata exported_polls_from_development_natural_keys.json
