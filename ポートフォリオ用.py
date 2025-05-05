## ライブラリをインポート

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

##　ブラウザ立ち上げ
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(options=options)
# browser = webdriver.Chrome()

# url取得
url = "https://barrierfree.pref.fukuoka.jp/"
# ブラウザー立ちあげ
browser.get(url)


browser.implicitly_wait(10)

## プログラム詳細

# csv出力用テキストデータを生成
n = 7  # 行数
m = 1  # 列数
# 空の2次元配列を初期化
output_data = [["" for _ in range(m)] for _ in range(n)]

idx = 0
# 「だれが」のボタン要素を取得
elements_who = browser.find_elements(By.XPATH, "//div[@class='who']/ul/li[*]/a")
for i, who in enumerate(elements_who):

    if i != 0:
            browser.get(url)

            # DOMを更新
            who = browser.find_elements(By.XPATH, "//div[@class='who']/ul/li[*]/a")[i]
    # 「だれが」ボタンをクリック
    who.click()

    # 「だれが」のテキストを取得
    who_text = who.find_element(By.XPATH, "p").text

    # 「なにする」のボタン要素を取得
    elements_what = browser.find_elements(By.XPATH, "//div[@class='what']/ul/li[*]/a")
    for j,what in enumerate(elements_what):

        if j != 0:
            browser.get(url)

            # DOMを更新
            who = browser.find_elements(By.XPATH, "//div[@class='who']/ul/li[*]/a")[i]
            what = browser.find_elements(By.XPATH, "//div[@class='what']/ul/li[*]/a")[j]

            who.click()
        # 「なにする」ボタンをクリック
        what.click()

        # 「なにする」のテキストを取得
        what_text_path = "//div[@class='what']/ul/li[{}]/a/div/span[2]".format(j+1)
        what_text = browser.find_element(By.XPATH, what_text_path).text

        # 「どこで」のエリア要素を取得
        elements_area = browser.find_elements(By.XPATH, "//div[@class = 'area-nav']/div/dl/dd")
        for k,area in enumerate(elements_area):

            if k != 0:
                browser.get(url)

                # DOMを更新
                who = browser.find_elements(By.XPATH, "//div[@class='who']/ul/li[*]/a")[i]
                what = browser.find_elements(By.XPATH, "//div[@class='what']/ul/li[*]/a")[j]
                area = browser.find_elements(By.XPATH, "//div[@class = 'area-nav']/div/dl/dd")[k]

                # ページ更新によってボタンが押されていないため再度押す
                who.click()
                what.click()

            # エリアテキストを取得
            elements_area_dt = browser.find_elements(By.XPATH, "//div[@class = 'area-nav']/div/dl/dt")
            elements_area_dt_text = elements_area_dt[k].find_element(By.XPATH, "a")
            area_text = elements_area_dt_text.text

            # タブリストが非表示の場合はクリックする
            if elements_area_dt[k].get_attribute("aria-selected") == "false":
                    elements_area_dt[k].click()
            
            # 「どこで」のボタン要素を取得
            elements_where = area.find_elements(By.XPATH, "ul/li[*]/a")

            for l, where in enumerate(elements_where):

                # １回目はこの処理を無視、２回目以降はブラウザを１段階戻す
                if l != 0:
                    # 最初のページを開く
                    browser.get(url)

                    # DOMを更新
                    who = browser.find_elements(By.XPATH, "//div[@class='who']/ul/li[*]/a")[i]
                    what = browser.find_elements(By.XPATH, "//div[@class='what']/ul/li[*]/a")[j]
                    elements_area_dt = browser.find_elements(By.XPATH, "//div[@class = 'area-nav']/div/dl/dt")
                    where_path = "//div[@class = 'area-nav']/div/dl/dd[{}]/ul/li[*]/a".format(k+1)
                    where = browser.find_elements(By.XPATH, where_path)[l]

                    # ページ更新によってボタンが押されていないため再度押す
                    who.click()
                    what.click()

                    # タブリストが非表示の場合はクリックする
                    if elements_area_dt[k].get_attribute("aria-selected") == "false":
                            elements_area_dt[k].click()

                # 「どこで」のテキストを取得
                where_text = browser.execute_script("return arguments[0].text;", where)
                where_text = where_text.replace('\n','')
                where_text = where_text.replace(' ','')

                # 「どこで」ボタンをクリック
                browser.execute_script('arguments[0].click();', where)

                # 「検索」のボタン要素を取得
                element_click = browser.find_element(By.CLASS_NAME, "btn-search")
                # 「検索」ボタンをクリック
                browser.execute_script('arguments[0].click();', element_click)

                # マップリスト要素を取得
                browser.implicitly_wait(1)
                elements_maplist = browser.find_elements(By.XPATH, "//ul[@class = 'map-spot-list']/li[*]/a")
                browser.implicitly_wait(10)

                # もしマップリストが無い場合
                if len(elements_maplist) == 0:
                    browser.get(url)
                    continue

                for o,map in enumerate(elements_maplist):
                    
                    # １回目はこの処理を無視、２回目以降はブラウザを１段階戻す
                    if o != 0:
                        browser.back()

                        # DOMを更新
                        map = browser.find_elements(By.XPATH, "//ul[@class = 'map-spot-list']/li[*]/a")[o]

                    # aタグのhrefからurlを取得
                    maplist_url = map.get_attribute("href")
                    # urlを開く
                    browser.get(maplist_url)

                    # データ要素を取得
                    elements_data = browser.find_elements(By.XPATH, "//div[@class='detail-info']/div[@class = 'data']/dl/dd[position() >= 0]")
                    # 「電話」テキストの有無確認用
                    elements_data_dt = browser.find_elements(By.XPATH, "//div[@class='detail-info']/div[@class = 'data']/dl/dt")

                    # csv用テキストデータ取得
                    if idx == 0:
                        # 「だれが」のテキストを取得
                        output_data[0][0] = who_text
                        # 「なにする」のテキストを取得
                        output_data[1][0] = what_text
                        # エリアテキストを取得
                        output_data[2][0] = area_text
                        # 「どこで」のテキストを取得
                        output_data[3][0] = where_text
                        # 施設名取得
                        output_data[4][0] = elements_data[0].text
                        # 住所取得
                        output_data[5][0] = elements_data[1].text
                        # 電話番号取得
                        for p in range(len(elements_data_dt)):
                            if elements_data_dt[p].text == "電話":
                                output_data[6][0] = elements_data[2].text
                                break
                            elif len(elements_data_dt)-1 == p:
                                output_data[6][0] = "-"
                        
                    else:
                        # 「だれが」のテキストを取得
                        output_data[0].append(who_text)
                        # 「なにする」のテキストを取得
                        output_data[1].append(what_text)
                        # エリアテキストを取得
                        output_data[2].append(area_text)
                        # 「どこで」のテキストを取得
                        output_data[3].append(where_text)
                        # 施設名取得
                        output_data[4].append(elements_data[0].text)
                        # 郵便番号取得
                        output_data[5].append(elements_data[1].text)
                        # 電話番号取得
                        for p in range(len(elements_data_dt)):
                            if elements_data_dt[p].text == "電話":
                                output_data[6].append(elements_data[2].text)
                                break
                            elif len(elements_data_dt)-1 == p:
                                output_data[6].append("-")
                    
                    if idx == 0:
                        idx += 1 

                    # csv出力データをコンソール上に表示
                    output_data_head = ["だれが","なにする","エリア","どこで","施設名","住所","電話番号"]
                    output_data_print =[who_text,what_text,area_text,where_text,elements_data[0].text,elements_data[1].text,elements_data[2].text]
                    for q in range(len(output_data_print)):
                         print("{0} = {1}".format(output_data_head[q], output_data_print[q])) 
print("fin")

# データフレームを作成
df = pd.DataFrame()
# データフレームにカラム追加
df['だれが'] = output_data[0]
df['なにを'] = output_data[1]
df['エリア'] = output_data[2]
df['どこで'] = output_data[3]
df['施設名'] = output_data[4]
df['住所'] = output_data[5]
df['電話番号'] = output_data[6]

# csvに出力
df.to_csv('福岡バリアフリーマップ.csv', index=False)

browser.close()