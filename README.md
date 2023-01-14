# journal_crawler
this is a code for export data from [libgen](https://libgen.rs/scimag/)

you should first install packages


```pip install -r requirement.txt```


after package installation, you must run the app

```python main.py -n {journal_id} -k {year_range}```

for journal id, you can search your journal in [libgen](https://libgen.rs/scimag/) and get journal_id from the url

for year range, you should enter you year range like this 2010-2020

it will export an excel(.xls) file in your home/exported_data/ directory
also there will be another directory, with your journal name, you can find all pdfs there.
