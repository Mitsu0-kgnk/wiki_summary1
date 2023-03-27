from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.chrome.options import Options
import re
import openai
import random

class wiki_summ:
    def __init__(self,word):
        self.word = word

    def scrayping(self):
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)
        kwd = self.word
        url = f'https://ja.wikipedia.org/wiki/{kwd}'

        driver.get(url)

        h1_tag = driver.find_element(By.TAG_NAME,'h1')
        # h1タグがキーワードと一致していれば検索成功
        if h1_tag.text != kwd:
            message = f'''
            ※『{kwd}』Wikipedia内にキーワードがありませんでした。
            以下を確認してみてください。
            ・誤字がないか（正式名称と合っているか）
            ・英単語の場合、頭文字が大文字になっているか
            ・漢数字かアラビア数字か
            '''
            f = open('summary.txt','w',encoding='utf-8')
            f.write(message)
            return message

        # print(driver.page_source)
        # 大枠と要素ごとに取得
        contents = driver.find_element(By.ID,'mw-content-text')
        contents = contents.find_element(By.CLASS_NAME,'mw-parser-output')
        tables = contents.find_elements(By.TAG_NAME,'table')
        uls = contents.find_elements(By.TAG_NAME,'ul')
        ols = contents.find_elements(By.TAG_NAME,'ol')
        divs = contents.find_elements(By.TAG_NAME,'div')
        h2s = contents.find_elements(By.TAG_NAME,'h2')
        h3s = contents.find_elements(By.TAG_NAME,'h3')
        h4s = contents.find_elements(By.TAG_NAME,'h4')

        ts = open('t-text.txt','w',encoding='utf-8')
        # 子要素を文字列として保存する
        for t in tables:
            ts = open('t-text.txt','a',encoding='utf-8')
            ts.write(f'{t.text}\n')
        for u in uls:
            ts = open('t-text.txt','a',encoding='utf-8')
            ts.write(f'{u.text}\n')
        for o in ols:
            ts = open('t-text.txt','a',encoding='utf-8')
            ts.write(f'{o.text}\n')
        for d in divs:
            ts = open('t-text.txt','a',encoding='utf-8')
            ts.write(f'{d.text}\n')
        ts = open('t-text.txt','r',encoding='utf-8')
        texts = ts.readlines()
        ts.close()

        sentences = contents.text
        # コンテンツ全体から不要な要素を除去する
        for line in texts:
            if line != '\n':
                sentences = sentences.replace(line,'')

        f = open('sentences.txt','w',encoding='utf-8')
        f.write(sentences)
        f.close()
        f = open('sentences.txt','r',encoding='utf-8')
        sentences = f.readlines()

        htags = []

        for h in h2s:
            htags.append(f'{h.text}\n')
        for h in h3s:
            htags.append(f'{h.text}\n')
        sentences = [line if line not in htags else '\n\n' for line in sentences]


        f = open('sentences.txt','w',encoding='utf-8')
        for t in sentences:
            f.write(t)
        # f.write(sentences)
        f.close()
        f = open('sentences.txt','r',encoding='utf-8')
        sentences = f.readlines()

        words = []
        features = []
        # 見出しごとに行を区切る
        for line in sentences:
            if line != '\n':
                s = line.rstrip('\n')
                s = re.sub("\[.+?\]", "", s)
                s = re.sub("\（.+?\）","",s)
                s = re.sub("\(.+?\)","",s)
                new = re.sub("[\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF65\u3000-\u303F]", '', s)
                words.append(s)
            else:
                features.append(words)
                words = []

        lists = features.copy()
        for i,l in enumerate(features):
            if len(l) <= 1:
                lists.remove(l)
                
        f = open('sentences.txt','w',encoding='utf-8')
        if len(lists) >= 5:
            num = 5
        else:
            num = len(lists)
        for l in random.sample(lists,k=num):
            s = ''.join(l)
            f.write(s)
        f.close()
        f = open('sentences.txt','r',encoding='utf-8')
        texts = f.read(2200)

        
        return texts




    def get_summary(self,input_text):
        openai.api_key = "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"

        # インプットテキスト

        # input_text = input_text
        kwd = self.word
        if input_text == f'''
            ※『{kwd}』Wikipedia内にキーワードがありませんでした。
            以下を確認してみてください。
            ・誤字がないか（正式名称と合っているか）
            ・英単語の場合、頭文字が大文字になっているか
            ・漢数字かアラビア数字か
            ''':
            return input_text

        def text_summary(prompt):
            # 分析の実施
            response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=500,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            )

            # 分析結果の出力
            # return response["choices"][0]["text"].replace('\n','')
            return response["choices"][0]["text"]

        # def crean_text(text):
        #     text= text.replace('　',' ')

        #     return text

        # 要約を5点で出力するように調整
        prompt ='''
        Tl;dr
        ポイントは以下の5点です。
        '''

        prompt = input_text +  prompt


        # 結果出力
        summary = text_summary(prompt)

        f = open('summary.txt','w',encoding='utf-8')
        f.write(summary)
        # print(summary)
        return summary

# w = wiki_summ('地球')
# w.get_summary(w.scrayping())


