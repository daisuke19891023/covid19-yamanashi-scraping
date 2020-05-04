# covid19-yamanashi-scraping

## What's this

covid-19に関する山梨県の公表済みのデータをスクレイピングにより取得するスクリプトです。

## Specification of Scraping

- [山梨県の新型コロナウィルス感染症公式ページ](https://www.pref.yamanashi.jp/koucho/coronavirus/info_coronavirus.html)よりサイトに表示する情報の元となるデータを取得する
- [新型コロナウイルス感染症に関する発生状況等](https://www.pref.yamanashi.jp/koucho/coronavirus/info_coronavirus_prevention.html)から取得するデータ
  - 陽性患者数
  - 陽性患者の属性
  - 個々の患者情報が記載されているPDFをテキストに変換し、データを取得する
- [新型コロナウイルス感染症に関する統計情報(発生状況、検査状況、相談件数)](https://www.pref.yamanashi.jp/koucho/coronavirus/info_coronavirus_data.html)から取得するデータ
  - 県内の疑似症例の検査状況
  - 帰国者・接触者相談センター相談件数
  - 新型コロナウイルス感染症専用相談ダイヤル相談件数


## Specification of Update

- 当リポジトリのGitHub Actions
  - GitHub Actionsにより毎時実行し、データに更新がある場合、`data.json`を更新する
  - データに変更があった場合、[対策サイトのGitHubリポジトリ](https://github.com/covid19-yamanashi/covid19)に対し`dispatch event`を発生させる
- dispatch先のリポジトリのGitHub Actions
  - `dispatch event`を受信し、`data.json`を更新した上でpull requestを出す
  - マージ元のブランチは`create-pull-request/patch`という名称で生成され、`default`ブランチへのマージを行う

## How to run

### Environment

- python version ≥ 3.7

### Set up command
```
$python -m pip install --upgrade pip

$pip install flake8 pytest pytest-cov "pytest-remotedata>=0.3.1"

$pip install -r requirements.txt
```
### Run command
スクリプト実行
```
$python -m src
```
テスト実行
```
$pytest -v --cov=.
```
## Where would it be used

- [山梨県 新型コロナウイルス感染症対策サイト](https://stopcovid19.yamanashi.dev/)
- https://github.com/covid19-yamanashi/covid19

## Lisence

本ソフトウェアは、[MITライセンス](./LICENSE)の元提供されています。

## Reference

- [長野県版 新型コロナウイルス感染症対策サイト データ更新を自動化した話](https://qiita.com/wataruoguchi/items/0f69f72777237674074b)
- https://github.com/wataruoguchi/covid19_nagano_csv_to_json