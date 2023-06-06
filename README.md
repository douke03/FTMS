# FTMS
## プロジェクト名について
チームの、チームによる、チームのためのタスク管理システム  
Task management system of the teams, by the teams, for the teams  
FTMS  
多分後で変更する。

## django環境の構築
色々インストールする。  
```
pip install Django
pip install django-crum
pip install django-sequences
```
証明書関連のエラーが出る場合は無視するための引数が沢山必要
```
pip --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install Django
```

多言語化対応に gettext が必要。  
https://stackoverflow.com/questions/35101850/cant-find-msguniq-make-sure-you-have-gnu-gettext-tools-0-15-or-newer-installed

## ローカルサーバの起動
```
python manage.py runserver --settings=config.settings.develop
```
## データベーステーブルの作成
```
python manage.py makemigrations
python manage.py migrate
```
## 管理ユーザーを作成する
```
python manage.py createsuperuser
```


## 多言語化対応
英語を日本語にした方がいろいろと都合がよさそう。
```
python -m django makemessages -l ja
python manage.py compilemessages
```
