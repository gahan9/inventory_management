Get database dump
```batch
python manage.py dumpdata --all --indent 4 -o <app-directory>/fixtures/data_dump.json
```

available flags to specify:

`--exclude=<app-name>.<model-name>` - exclude any model

`-e contenttypes` - exclude app and it's migration from dump
        (contenttypes avoided to prevent error while loading fixtures)


Execute Test
```batch
python manage.py test inventory_management.tests.LoginTestSelenium
```

venv activate:
Windows powershell user might need to execute below command:
```
Set-ExecutionPolicy RemoteSigned
```
before executing  `venv\Scripts\activate`