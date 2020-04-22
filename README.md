# ptxconf
PTXconf を日本語化したものになります。

複数のモニタを利用する場合に、ペンのマッピング先を切り替えるツールとなります。

マニュアルは、次にあります。

[wenhsinjen.github.io/ptxconf/](http://wenhsinjen.github.io/ptxconf/)

以下マニュアルから抜粋しました。

１．依存ライブラリインストール

次の依存ファイルをインストールします。

$ sudo apt-get install xinput x11-xserver-utils 

$ sudo apt-get install python-gtk2, python-appindicator  python-pip



２．PTXCONFインストール

$ sudo pip install  https://github.com/megamuteki/ptxconf/archive/master.zip 



3.ptfconf.desktop作成（例）

echo "[Desktop Entry]

Version=0.1.0 

Encoding=UTF-8

Name=ptxconf

Comment=ペンマッピング

Exec=/usr/local/bin/ptxconf.py

Icon=video-display

StartupNotify=true

Terminal=false

Type=Application

Categories==System;Settings;" | sudo tee -a  /usr/share/applications/ptxconf.desktop



4.PTXCONFアンインストール

$sudo -H pip uninstall  ptxconf 

$sudo rm  -f  /usr/share/applications/ptxconf.desktop
	

5.解説

Pen tablet and Touch screen Xinput Configuration tool (PTXConf). Configures touch/pen devices to work with extended desktops and multiple screens on Linux.
Please find the installation and usage instructions in the documentation located here: [wenhsinjen.github.io/ptxconf/](http://wenhsinjen.github.io/ptxconf/)

WenHsin Linda Jen 2015



## サンプルの写真

memo:ptxconfスタート画面

![ptxconf](https://github.com/megamuteki/images/blob/master/ptxconf/ptxconf01.png)



memo:ptxconf設定画面

![ptxconf](https://github.com/megamuteki/images/blob/master/ptxconf/ptxconf02.png)



memo:ペンタブレットメニュー 選択画面

![ptxconf](https://github.com/megamuteki/images/blob/master/ptxconf/ptxconf03.png)



