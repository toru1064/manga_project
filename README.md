# 漫画感想アプリ（Flask）

## 概要

このアプリは、好きな漫画に対して感想や評価を投稿・共有できるWebアプリケーションです。
PythonのWebフレームワーク「Flask」を使用して開発しました。

ユーザー登録・ログイン、投稿、いいね、コメント、プロフィール、ランキング、検索など、基本的なWebアプリケーション機能を実装しています。

## 主な機能

* ユーザー登録 / ログイン機能
* 投稿機能（タイトル・感想・評価）
* 投稿の編集 / 削除
* 投稿一覧表示
* いいね機能（トグル）
* コメント機能
* プロフィール機能（名前・自己紹介・画像）
* ランキング機能（いいね数・評価）
* 検索機能（タイトル・感想）
* Google Books APIを利用した漫画検索機能（実装途中）

## 使用技術

* Python 3.x
* Flask
* Flask-Login
* Flask-SQLAlchemy
* Flask-Migrate
* HTML / CSS
* Jinja2
* SQLite
* Google Books API
* Gunicorn
* AWS Elastic Beanstalk
* Git / GitHub

## デプロイ状況

### Render

Render用ブランチを作成し、既存のRender環境はそのブランチを参照する形で維持しています。

### AWS Elastic Beanstalk

AWS Elastic Beanstalkを使用して、Flaskアプリケーションをデプロイしました。

現在のAWS環境では、以下の構成で動作確認を行っています。

* AWS Elastic Beanstalk
* Python 3.11
* Gunicorn
* Nginx
* SQLite（一時的な動作確認用）

また、EB CLIを導入し、手動でzipファイルをアップロードする方式から、以下のコマンドでデプロイできるようにしました。

```bash
eb deploy
```

## 現在の注意点

現在のAWS環境ではSQLiteを使用しているため、Elastic BeanstalkのデプロイやEC2インスタンスの再作成時に、登録ユーザーや投稿データが消える可能性があります。

そのため、現時点ではAWS上でのアプリ起動確認・動作確認を目的とした構成です。
今後、Amazon RDS PostgreSQLへ移行し、デプロイ後もデータが保持される構成へ改善する予定です。

また、Google Books API連携機能は実装途中です。
現在はAPIへリクエストする処理まで実装していますが、APIキーの環境変数管理や検索結果の投稿フォーム連携は今後対応予定です。

## 画面イメージ

準備中（スクリーンショットを後で追加予定）

## インストール方法

```bash
git clone https://github.com/toru1064/manga_project.git
cd manga_project/manga_app

python -m venv venv
```

Windowsの場合：

```bash
venv\Scripts\activate
```

必要なライブラリをインストールします。

```bash
pip install -r requirements.txt
```

アプリを起動します。

```bash
flask run
```

## 今後の改善予定

* SQLiteからAmazon RDS PostgreSQLへの移行
* データベース接続情報の環境変数化
* Google Books APIキーの環境変数管理
* Google Books APIの検索結果を投稿フォームへ連携
* 投稿時に表紙画像・著者情報を自動反映
* GitHub Actionsによる自動デプロイの導入
* スクリーンショットの追加
* AWS構成図の追加