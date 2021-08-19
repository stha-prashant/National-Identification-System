# National-Identification-System
<hr>
### Installing dependencies
First install conda

# Todo:

### Running the website
First make all necessary migrations from inside the `NID` folder
```
python manage.py makemigrations accounts
python manage.py makemigrations documents 
python manage.py makemigrations address 
python manage.py migrate
```

Then from inside `NID` folder
```
python manage.py runserver
```


