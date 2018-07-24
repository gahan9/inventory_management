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

Features:
- Purchase Records
- Sale Records
- Generate Invoice
- Dynamic Tax Invoice
- Stock management
- Email integrated (for web user)

Features in Detail:
Data Entry

    Purchase details
    Sale Details
        discout calculation
        by item calculation
        overall GST invoice (to be discussed.. for overall or by item)

Reports

    Filter by mobile brand
    Credit/Debit report
    Filter by IMEI of device
    Find out customer detail by name/number/address or IMEI number

Other

    GST invoice (to be discussed.. category vise GST??)
    Invoice generation for printing

GST flow:

    add during product addition in system
    add during sale
