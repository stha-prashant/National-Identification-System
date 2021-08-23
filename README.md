# [National-Identification-System](https://nid.pythonanywhere.com)
<hr>

### Installing dependencies
Run from inside project root (National-Identification-System) folder
```bash
pip install -r envs/requirements.txt
```
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


