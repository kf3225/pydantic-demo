# pydantic-demo

pydantic をお試しで使ってみました

## 事前準備

### 必要ツール

- rye

### セットアップ

1. `git clone`する

   ```
   git clone https://github.com/kf3225/pydantic-demo.git
   cd pydantic-demo
   ```

1. `rye sync`し必要ライブラリをインストール

   ```
   rye sync
   ```

## 動作確認

1. `rye run test`で動作確認

   ```
   rye run test
   ================================================================================== test session starts ==================================================================================
   platform darwin -- Python 3.11.3, pytest-7.4.0, pluggy-1.2.0 -- /Users/k/workspace/pydantic-demo/.venv/bin/python
   cachedir: .pytest_cache
   rootdir: /Users/k/workspace/pydantic-demo
   collected 1 item

   tests/pydantic_demo/test_main.py::TestMain::test_main_succeeded setup
   PASSEDteardown


   =================================================================================== 1 passed in 0.19s ===================================================================================
   ```

## 所感

- dataclass よりリッチな機能が提供されているが、初見でコードリーディングするのはコストが高そう
  - とはいえ FastAPI に組み込まれていることから考えると Python で Web API 開発している人にとっては容易く読み書きできる？
- json ファイルのアウトプット機能など、ユーティリティ機能を持たせるには`BaseModel`を継承した独自クラスを作り、そこに json ファイルを出力できる`output`メソッドを実装。その後ユーティリティ機能付きクラスをモデルクラスに継承した
  - こんな使い方であってるのだろうか…
- TODO として pyspark との組み合わせが便利そうか確認したい
  - 特に validator 周り(pyspark での実装がつらい部分)
