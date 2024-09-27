## 認証方式検討

- RESTfulなAPIでは**JWT認証を採用する**のが適しているとされている

<div style="overflow-x:auto;">

| 認証方式 | トークンの形式 | 概要 | メリット | デメリット | 備考 |
| --- | --- | --- | --- | --- | --- |
| Basic認証 | トークン自体にユーザー情報が含まれる | ユーザー名とパスワードをBase64エンコードしたものを利用。セキュリティ面で弱いため、Webアプリケーションの認証方式としては不適。 | 簡単に認証情報を準備できる | セキュリティ的に問題がある | |
| Cookie認証 | サーバー側でランダムな文字列を発行してサーバー側の管理用テーブルと突合 | サーバー側のセッション情報を保存し、CookieでセッションIDを管理。 | 認証情報の送信が自動化される | サーバーで状態を管理するためREST(ステートレス)に反する | |
| Token認証 | サーバー側でランダムな文字列を発行してサーバー側の管理用テーブルと突合 | トークンを発行してユーザーのログイン状態を管理。 | CSRF対策が不要（localStorageなどにトークンを保存可能） | トークンがWebストレージに残り続けるため、再作成などのセキュリティ対策が必要 | |
| JWT認証 | トークン自体にユーザー情報が含まれる | 認証情報を含むJSON形式のデータをエンコードしたトークン。 | データベースにトークンを保存する必要がなく、サーバー側で状態管理不要 | クライアント側の実装がやや複雑 | dj-rest-auth + simplejwt での実装が推奨される |

</div>

## エンドポイント一覧

<div style="overflow-x:auto;">

| 用途 | HTTPメソッド | エンドポイント | コマンド例 |
| --- | --- | --- | --- |
| ログイン(トークン取得) | POST | api/auth/login/ | `http POST http://127.0.0.1:8081/api/auth/login/ email="doinkya0@gmail.com" password="password_"` |
| ログアウト | POST | api/auth/logout/ | `http POST http://127.0.0.1:8081/api/auth/logout/` |
| ユーザーデータ取得 | GET | api/auth/user/ | `http GET http://127.0.0.1:8081/api/auth/user/ "Authorization: JWT <your_access_token>"` |
| パスワードリセットリクエスト | POST | api/auth/password/reset/ | `http POST http://127.0.0.1:8081/api/auth/password/reset/ email="user@example.com"` |
| パスワードリセット確認 | POST | api/auth/password/reset/confirm/ | `http POST http://127.0.0.1:8081/api/auth/password/reset/confirm/ uid="UID" token="TOKEN" new_password="new_password"` |
| トークンの検証 | POST | api/auth/token/verify/ | `http POST http://127.0.0.1:8081/api/auth/token/verify/ token="your_access_token"` |
| トークンの再取得(リフレッシュ) | POST | api/auth/token/refresh/ | `http POST http://127.0.0.1:8081/api/auth/token/refresh/ refresh="your_refresh_token"` |
| パスワード変更 | POST | api/auth/password/change/ | `http POST http://127.0.0.1:8081/api/auth/password/change/ "Authorization: JWT <your_access_token>" old_password="old_password" new_password1="new_password" new_password2="new_password"`

</div>

## 実現できていないこと

- 一部エンドポイントの完成(メール認証のリダイレクト、パスワード変更)
- models.pyとの連携
    - 現在の状況では、ユーザー登録時に作成されているモデルはカスタムの User モデルだが、dj-rest-auth や Django REST Framework で使用される認証関連の機能は、Djangoが提供する django.contrib.auth.models.User モデルに依存している。
    - このため、カスタム User モデルを使って登録したユーザー情報を登録する一方で、Django標準の User モデルにユーザーが登録されていない実装に齟齬がある状態。
    - もし、カスタム User モデルを使用する場合は、Djangoの認証システムと互換性のある形で実装する必要がある。これは AbstractBaseUser や PermissionsMixin を使ってカスタムユーザーモデルを構築する必要がある。
- postmanを使ったテスト←やるべきか相談

## 参考記事

[1] 現場で使えるDjango REST Frameworkの教科書. 横瀬 明仁. 2023.

[2] [**Django REST APIs with JWT Authentication using dj-rest-auth](https://medium.com/@michal.drozdze/django-rest-apis-with-jwt-authentication-using-dj-rest-auth-781a536dfb49)** ← ログインやJWT認証全般

[3] [**Django REST framework JWT Authentication Sign up API with email confirmation.](https://medium.com/@michal.drozdze/django-rest-framework-jwt-authentication-sign-up-api-with-email-confirmation-0cfc6054ce8e)** ← メール検証