# 漫画感想アプリ（Flask）

## 概要

このアプリは、好きな漫画に対して感想や評価を投稿・表示できるWebアプリケーションです。  
PythonのWebフレームワーク「Flask」を使用して開発しました。

## 主な機能

- 漫画のタイトル・感想・評価を投稿
- 投稿一覧を表示
- （予定）ログイン機能、データベース保存、編集・削除機能など

## 使用技術

- Python 3.x
- Flask
- HTML / Jinja2
- Git / GitHub

## 画面イメージ

準備中（スクリーンショットなどをここに貼る予定）

## インストール方法

```bash
git clone https://github.com/toru1064/manga_project.git
cd manga_project/manga_app
python -m venv venv
source venv/bin/activate  # Windows の場合: venv\Scripts\activate
pip install -r requirements.txt
python run.py