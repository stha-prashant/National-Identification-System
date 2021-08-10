# National-Identification-System
<hr>

### Installing dependencies
First install conda

Then run following commands in given order from project folder(National-Identification-System folder)
```bash
conda create --name DBMS --file NID/envs/requirements.txt
conda deactivate & conda activate DBMS
pip install -r NID/envs/pip_requirements.txt
```

### Running the website
First make all necessary migrations from inside teh `NID` folder
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