## ユーザー向けドキュメント

TBW

## 開発者向けドキュメント

TBW

- prefix_url + でok
- 学外からの電子ソースにだけ存在して、他にいないやつがいる
  - 今後もこの要件を満たす必要がある

## データベース設計

データベースは `master.xlsx` という名前でプロジェクト直下に保存する。

### データベース

シート名は `database`

|カラム名|説明|
|-|-|
|id||
|name||
|url||
|is_available_remote||
|available_area_id||
|simultaneous_connections||
|name_en||
|guide_en||

### カテゴリー

シート名は `category`

|カラム名|説明|
|-|-|
|id||
|name||
|name_en||

### カテゴリーリレーション

シート名は `category_relation`

|カラム名|説明|
|-|-|
|database_id||
|category_id||

### 利用可能エリア

"学内", "学外", "公開", "鶴舞大幸"などの情報と、行の背景色を決定する。

シート名は `available_area`

|カラム名|説明|
|-|-|
|id||
|name||
|name_en||
|background_color||
