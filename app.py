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
