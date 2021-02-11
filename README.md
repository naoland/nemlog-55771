nemlog-55771

# 【TIPS#6】 TermuxでWEBアプリを作ってアクセスしてみる 

## はじめに

今回はご自身のAndroidスマホで上で簡単なWEBアプリを起動して、スマホのブラウザからアクセスしてみたり、PCのブラウザからアクセスしてみる方法をご紹介します。

Zaif取引所のXEMの最終価格を表示するだけのシンプルなWEBアプリです。

## WEBアプリケーションの起動準備

Pythonの仮想環境をインストールします。Pythonのインストールやセットアップが終わってない方は過去記事をご参照ください。

```
$ python -m venv venv
```

これで`venv`というディレクトリができたはずです。

この仮想環境を有効にします。

```
source ./venv/bin/activate
```

仮想環境を終了する場合は、たんに`deactivate'とタイプしてください。


仮想環境にWEBフレームワーク`Bottle`をインストールします。

```
$ pip install bottle
```

実行例

```
nemlog-55771 main $ pip install bottle
Collecting bottle
  Downloading bottle-0.12.19-py3-none-any.whl (89 kB)
     |████████████████████████████████| 89 kB 422 kB/s 
Installing collected packages: bottle
Successfully installed bottle-0.12.19
```

一般的にはDjangoやFlaskといったフレームワークが人気ですが、この記事では軽量で高速な`Bottle`を使用します。Bottleは私のお気に入りでもあります。


このアプリではZaifで取り扱っている暗号資産の最終価格を表示します。
Zaifが提供しているAPIへアクセスするためのモジュールをインストールします。

```
$ pip install zaifapi
```
実行例

```
nemlog-55771 main $ pip install zaifapi
Collecting zaifapi
  Downloading zaifapi-1.6.3.tar.gz (8.5 kB)
Collecting requests
  Using cached requests-2.25.1-py2.py3-none-any.whl (61 kB)
Collecting websocket-client
  Downloading websocket_client-0.57.0-py2.py3-none-any.whl (200 kB)
     |████████████████████████████████| 200 kB 198 kB/s 
Collecting Cerberus
  Downloading Cerberus-1.3.2.tar.gz (52 kB)
     |████████████████████████████████| 52 kB 93 kB/s 
Requirement already satisfied: setuptools in ./venv/lib/python3.8/site-packages (from Cerberus->zaifapi) (49.2.1)
Collecting certifi>=2017.4.17
  Using cached certifi-2020.12.5-py2.py3-none-any.whl (147 kB)
Collecting chardet<5,>=3.0.2
  Using cached chardet-4.0.0-py2.py3-none-any.whl (178 kB)
Collecting idna<3,>=2.5
  Using cached idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.3-py2.py3-none-any.whl (137 kB)
     |████████████████████████████████| 137 kB 225 kB/s 
Collecting six
  Using cached six-1.15.0-py2.py3-none-any.whl (10 kB)
Using legacy 'setup.py install' for zaifapi, since package 'wheel' is not installed.
Using legacy 'setup.py install' for Cerberus, since package 'wheel' is not installed.
Installing collected packages: urllib3, six, idna, chardet, certifi, websocket-client, requests, Cerberus, zaifapi
    Running setup.py install for Cerberus ... done
    Running setup.py install for zaifapi ... done
Successfully installed Cerberus-1.3.2 certifi-2020.12.5 chardet-4.0.0 idna-2.10 requests-2.25.1 six-1.15.0 urllib3-1.26.3 websocket-client-0.57.0 zaifapi-1.6.3
```

## WEBアプリの起動

次のようにタイプします。 `app.py` は`Python言語で書かれた`WEBアプリのソースコードです。

```
$ python app.py
```

実行例

```
nemlog-55771 $ python app.py
Bottle v0.12.19 server starting up (using WSGIRefServer())...
Listening on http://0.0.0.0:8080/
Hit Ctrl-C to quit.
```

終了する場合は`Ctrl-C`（コントロールキーを押しながらCを押します）をタイプしてください。


## WEBアプリの動作確認

スマホのブラウザで確認する場合

http://localhost:8080/last_price/xem_jpy


<img src="https://i.gyazo.com/483bc2879ee2bce27d28f7272e31f136.png" alt="キーボードが非表示状態（縦）" width="40%"/>  


PCのブラウザで確認する場合

http://スマホのIPアドレス:8080/last_price/xem_jpy



![](https://i.gyazo.com/ad44e24e0103f087b7a21add67cbdbb0.png)


この例ではIPアドレスが`192.168.1.3`になっています。


スマホのIPアドレスは次のコマンドで確認できます。

```
$ ip -4 a | grep inet
```
実行例

```
nemlog-55771 main $ ip -4 a | grep inet
    inet 127.0.0.1/8 scope host lo
    inet 192.168.1.4/24 brd 192.168.1.255 scope global dynamic noprefixroute enp1s0
    inet 172.17.0.1/16 brd 172.17.255.255 scope global docker0
    inet 172.18.0.1/16 brd 172.18.255.255 scope global br-92e7b478080d
```

## ソースコード

```python
# app.py
from bottle import route, run, template
from zaifapi import ZaifPublicApi, ZaifFuturesPublicApi, ZaifLeverageTradeApi


@route("/")
def index():
    return "<h1>Hello World!</h1>"


@route("/hello/<name>")
def index2(name):
    return template("<h1>Hello {{name}}!</h1>", name=name)


@route("/last_price/<pair>")
def last_price(pair):
    """指定した通貨ペア（xem_jpyなど）の最終価格を表示します。"""
    zaif = ZaifPublicApi()
    result = zaif.last_price(pair)
    print(result)
    return template(
        "<h1>{{pair}} 最終価格: {{result}}</h1>", pair=pair, result=result["last_price"]
    )

# host_address = "localhost"
host_address = "0.0.0.0"

# アプリケーションサーバーを起動します。
# ホストのアドレスが 0.0.0.0 の場合は、ローカルネットワークのどのPCからでもアクセスできます
# そのため、公衆無線LANでは、localhostを使用するようにしましょう。それによって、スマホ内のブラウザからのみアクセスできるようになります。
run(host=host_address, port=8080, debug=True, reloader=True)

```

## まとめ

いかがでしたでしょうか？

自分のスマホがWEBアプリケーションサーバーなりました！

この記事では`Zaif`で取り扱っている暗号資産の最終価格を表示するだけのシンプルな機能をもったWEBアプリをご紹介しましたが、もちろん頑張ってコードを書けば本格的なWEBアプリケーションを作ることも可能です。

ぜひトライしてみてください！


## 関連情報へのリンク

- [Bottle: Python Web Framework](https://bottlepy.org/docs/dev/)
