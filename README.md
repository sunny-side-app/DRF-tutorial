## 認証方式検討

- RESTfulなAPIでは**JWT認証を採用する**のが適しているとされている

| 認証方式 | トークンの形式 | 概要 | メリット | デメリット | 備考 |
| --- | --- | --- | --- | --- | --- |
| Basic認証 | トークン自体にユーザー情報が含まれる | ユーザー名とパスワードをBase64エンコードしたものを利用。セキュリティ面で弱いため、Webアプリケーションの認証方式としては不適。 | 簡単に認証情報を準備できる | セキュリティ的に問題がある | |
| Cookie認証 | サーバー側でランダムな文字列を発行してサーバー側の管理用テーブルと突合 | サーバー側のセッション情報を保存し、CookieでセッションIDを管理。 | 認証情報の送信が自動化される | サーバーで状態を管理するためREST(ステートレス)に反する | |
| Token認証 | サーバー側でランダムな文字列を発行してサーバー側の管理用テーブルと突合 | トークンを発行してユーザーのログイン状態を管理。 | CSRF対策が不要（localStorageなどにトークンを保存可能） | トークンがWebストレージに残り続けるため、再作成などのセキュリティ対策が必要 | |
| JWT認証 | トークン自体にユーザー情報が含まれる | 認証情報を含むJSON形式のデータをエンコードしたトークン。 | データベースにトークンを保存する必要がなく、サーバー側で状態管理不要 | クライアント側の実装がやや複雑 | dj-rest-auth + simplejwt での実装が推奨される |
※上記内容は[1]より引用

- 認証用トークンの格納先はCookie/localStorage/sessionStorageのどれを使うべきか

→ 下記いずれかが望ましい

- httpOnly属性を付与してSet-Cookieヘッダで受け取ったトークンをCookieに保存してCSRF対策を行う
- 有効期限のあるトークンをlocalStorageに保存してXSS脆弱性に気を付ける

(sessionStorageだとタブごとの保存領域であるためタブを複製した場合にログインが切れてしまい不便)

※上記内容は[1]より引用

- **エンドポイントの追加:**
    - `dj-rest-auth`で様々なエンドポイント（ユーザー登録、パスワード変更、ソーシャル連携など）を追加可能。

## エンドポイント一覧

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

## 参考記事

[1] 現場で使えるDjango REST Frameworkの教科書. 横瀬 明仁. 2023.

[2] [**Django REST APIs with JWT Authentication using dj-rest-auth](https://medium.com/@michal.drozdze/django-rest-apis-with-jwt-authentication-using-dj-rest-auth-781a536dfb49)** ← ログインやJWT認証全般

[3] [**Django REST framework JWT Authentication Sign up API with email confirmation.](https://medium.com/@michal.drozdze/django-rest-framework-jwt-authentication-sign-up-api-with-email-confirmation-0cfc6054ce8e)** ← メール検証
```
