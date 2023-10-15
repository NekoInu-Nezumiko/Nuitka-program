#zipcloudのAPIを用いたアプリ制作:setfocusを入れる
"""
仮想環境の作り方(仮想環境で実施する)
pipenv --three 作成
pipenv shell 入る
exit 出る
pipenv install package パッケージインストール:必要なモノ

zstandard:圧縮率OK --onefileでまとめる時
nuitka --mingw64 --follow-imports --plugin-enable=tk-inter --onefile test4.py
"""

def main():
    #いつもの解像度変更
    import ctypes
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    import PySimpleGUI as sg
    import requests
    sg.theme("Default1")
    """focus=Trueで立ち上がったタイミングでのfocus"""
    layout = [
        [sg.Text("郵便番号:"),
         sg.InputText(key="-NUMBER1-", size=(10,3),focus=True),
         sg.Text("-"),
         sg.InputText(key="-NUMBER2-", size=(10,3)),   
        ],
        [sg.Text("住所:",size=(5,5)),
         sg.InputText(key="-ADDRESS-", size=(20,5)),
        ],
        [sg.Button("実行", key="-SUBMIT-")],
    ]

    window = sg.Window("test_number",layout,size=(600,600),return_keyboard_events=True)

    while True:
        event, values = window.read()
        #Enterキーが押された際の処理
        if event in ("\r","special 16777220", "special 16777221"):
            elem = window.FindElementWithFocus()#どこにFocusがいっているか取得
            if elem.Key == "-NUMBER1-":
                window.Element("-NUMBER2-").SetFocus()#フォーカスを移す
            elif elem.Key == "-NUMBER2-":
                event = "-SUBMIT-" #実行ボタンを押したものとする

        if event == "-SUBMIT-":
            """入力値を取得"""
            num1 = values["-NUMBER1-"] #3桁
            num2 = values["-NUMBER2-"] #4桁
            """requestsを送信"""
            URL = "https://zipcloud.ibsnet.co.jp/api/search"
            res = requests.get(f"{URL}",params={"zipcode":f"{num1}{num2}"})
            res_json = res.json()

            """正常に取得出来たら:ない場合でも取得できることがあるのでNoneの場合もelseへ"""
            if res_json["status"] == 200 and res_json["results"] != None:
                result = res_json["results"][0]
                adr1 = result["address1"]#都道府県
                adr2 = result["address2"]#市区町村
                adr3 = result["address3"]#町域

                #代入
                window["-ADDRESS-"].update(value=f"{adr1}{adr2}{adr3}")
            else:
                window["-ADDRESS-"].update(value="住所の取得に失敗")

        if event == sg.WIN_CLOSED:
            break

if __name__ == "__main__":
    main()

