# FTMS
## プロジェクト名について
チームの、チームによる、チームのためのタスク管理システム  
Task management system of the teams, by the teams, for the teams  
FTMS  
多分後で変更する。

## django環境の構築
色々インストールする。  
証明書関連のエラーが出るので無視するための沢山引数が必要
```
pip install Django
pip --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install Django

pip install django-crum
pip --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org install django-crum

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
