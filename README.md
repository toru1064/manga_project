# 漫画感想アプリ（Flask）

## 概要

このアプリは、好きな漫画に対して感想や評価を投稿・共有できるWebアプリケーションです。  
PythonのWebフレームワーク「Flask」を使用して開発しました。

## 主な機能

- ユーザー登録 / ログイン機能
- 投稿機能（タイトル・感想・評価）
- 投稿の編集 / 削除
- 投稿一覧表示
- いいね機能（トグル）
- コメント機能
- プロフィール機能（名前・自己紹介・画像）
- ランキング機能（いいね数・評価）
- 検索機能（タイトル・感想）

## 使用技術

- Python 3.x
- Flask
- Flask-Login
- Flask-SQLAlchemy
- HTML / Jinja2
- SQLite
- Git / GitHub

## 画面イメージ

準備中（スクリーンショットを後で追加予定）

## インストール方法

```bash
git clone https://github.com/toru1064/manga_project.git
cd manga_project/manga_app

python -m venv venv
# Windowsの場合
venv\Scripts\activate

pip install -r requirements.txt
python run.py