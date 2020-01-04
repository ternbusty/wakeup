# wakeup

## 概要

-   [WebIOPi](https://webiopi.trouch.com/) を用いてラズパイを Web サーバ化し、同じネットワーク上にある他の機器から布団自動引き剥がし時刻を設定できるようにするためのスクリプト
-   設定ページにアクセスすると、現在の引き剥がし設定時刻が表示される
-   `Time configuration` 欄に時刻を入力して submit すると、ラズパイの crontab に引き剥がしのタスク (`#lock`) が設定される。さらに、その３時間後にあたる時刻に逆回転を行うタスク (`#unlock`) が設定される。
-   `Time configuration` 欄を空白にして submit すると、crontab 上の `#lock` および `#unlock` のコメントがついたタスクが取り消される

## 導入

以下の記述は [こちら](https://raspibb.blogspot.com/) を参考にしている。

-   [こちら](https://webiopi.trouch.com/DOWNLOADS.html) から、Cayenne ではなく WebIOPi-0.7.1.tar.gz をダウンロードし、 `/home/pi` に展開する
-   WebIOPi のインストール

```shell
cd WebIOPi-0.7.1/
wget https://raw.githubusercontent.com/neuralassembly/raspi2/master/webiopi-pi2bplus.patch
patch -p1 -i webiopi-pi2bplus.patch
sudo ./setup.sh
```

-   本レポジトリをクローンし、WebIOPi のコンテンツ用ディレクトリ `/usr/share/webiopi/htdocs` にコピーする

```shell
git clone https://github.com/iwasaki501/wakeup.git
sudo chown -R pi /usr/share/webiopi/htdocs
cp -r wakeup /usr/share/webiopi/htdocs
```

-   WebIOPi 設定ファイルの編集

```shell
sudo leafpad /etc/webiopi/config
```

とし、`[SCRIPTS]` セクションに次のように一行追記して保存

```
#myscript = /home/pi/webiopi/examples/scripts/macros/script.py
myscript = /usr/share/webiopi/htdocs/wakeup/script.py
```

-   [python_crontab](https://pypi.org/project/python-crontab/) モジュールのインストール

```shell
sudo pip3 install python-crontab
```

## 実行

-   debug モードで実行

```shell
sudo webiopi -d -c /etc/webiopi/config
```

-   同じネットワーク上の他の機器からは `http://raspberrypi.local:8000/wakeup/` でアクセスできる

## トラブルシューティング

-   debug モードで実行しようとすると `address already in use` エラーが出るときは、

```shell
sudo netstat -antp
```

で状態が `LISTEN`、`PID/Program name` が `xxxx/python3` となっているプロセスを発見し、

```shell
sudo kill -9 xxxx
```

とする

## その他

styles.css については [こちら](https://deshinon.com/2019/03/03/oshare-kopipe-login-css/) を改変したものを使用している
