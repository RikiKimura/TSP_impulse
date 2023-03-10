##  Readme  ##

【名称】
　TSPインパルス応答測定

【概要】
  TSPを用いてインパルス応答を導出するスクリプト
  TSP作成 → Play＆Rec → インパルス応答導出 → 保存(binary-64bit) のフローが実行される

【動作環境】
  ■OS
    ・Windows

  ■Python
    ・Python 3.X ＆ sounddeviceのpip版(Conda不可)

  ■デバイス
    ・ASIO等で再生・録音ができるオーディオインターフェイス又はそれに準ずるもの

【事前準備】
    ・オーディオデバイスのドライバを入れて、適宜バッファ調整などをしておく(サンプルレートも同じ値にする)
    ・コンプレッサーなどのHWエフェクトを無効化する
    ・オーディオストリームをブロックするセキュリティソフトは一時停止する

【使用方法】
  ■GUIを使う場合
    1.GUI.pyを実行する
    2.GUIが立ち上がったら、「デバイス番号確認」を押してデバイス番号を調べる
    3.各フォームを半角英数で埋める
    4.「測定開始」を押して測定する

  ■直接実行する場合
    1.エディタでTSP_impulse.pyを開く
    2.各種パラメータを入力する
    3.スクリプトを実行して測定する
    
【注意事項】
    ・データはオーディオバッファ等に起因する遅延を含む
    ・2CHまでの対応(3CH以上のデバイスを指定しても1・2CH目までしか動作しない)
    ・測定中に強制終了するとオーディオデバイスをリセットするまで動作しないことがある
