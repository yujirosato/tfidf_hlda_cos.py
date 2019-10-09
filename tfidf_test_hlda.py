#あるホテルのレビューを月ごとに文書集合を作成
#特定の月に出現した名詞に対してtfidfを付与

import csv
import MeCab
from gensim import corpora
from gensim import models
from pprint import pprint # オブジェクトを整えて表示するライブラリ. gensimのtfidf計算には不要

import os#ディレクトリ操作をするライブラリ
stop_words = ["*", "TWNROOM", "cc"]

#
# def morphological_analysis():#形態素解析する関数
#

#文字列に数字が含まれているものを判別する
def hasNumbers(inputString):

    return any(char.isdigit() for char in inputString)

def make_doc(hotel_code):

    dic_documents = {"01": "", "02": "","03": "","04": "","05": "","06": "",
                 "07": "","08": "","09": "","10": "","11": "","12": ""}#１２ヶ月分の文書集合

    print(hotel_code +  " : " + month)
    # print(os.getcwd())

    #データがあるディレクトリに移動
    os.chdir("/Users/satouyujirou/kennkyuu/rakutenrebyu/M1/review_data")

    #NeologD辞書を使用　# 形態素解析器の変数（オブジェクト）を作成
    t = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')

    for num in range(12):
        filename = "0" + str(num) + ".csv"

        if num > 9:
             filename = str(num) + ".csv"

        print(filename)

        ############################file_open#####################
        with open(filename, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:#一行づつ処理

                line_div = line.split(",")#{0:code, 1:日時(ex.1997/01/14), 2:投稿時間, 3:レビュー}

                if hotel_code == line_div[0]:#hotel番号が一致した場合のみ処理する

                    line_month = line_div[1].split("/")#{0:年, 1:月, 2:日にち}

                    line_doc = t.parse(line_div[3])#レビューの形態素解析
                    word = [word.replace('\t',',').split(',') for word in line_doc.split('\n')[:-2]]#形態素解析データを分割してリストに
                    ####################
                    #word = {['この', '連体詞', '*', '*', '*', '*', '*', 'この', 'コノ', 'コノ'],
                    #        ...}
                    ####################
                    for sec in word:
                        #英語, ストップワード, 数字を除外
                        if sec[1] == "名詞" and hasNumbers(sec[7]) == False and sec[7] not in stop_words and sec[7].isalpha() == True:
                            #名詞の原型を抽出, パッケージに入れれるようにデータの形を整える
                            if len(dic_documents[line_month[1]]) == 0:
                                dic_documents[line_month[1]] = sec[7]
                            else:
                                dic_documents[line_month[1]] = dic_documents[line_month[1]] + " " + sec[7]




                line = f.readline()

        ##########################################################
    documents = []#最終的なドキュメント集合

    for num in range(12):
        documents_month = "0" + str(num + 1)

        if (num + 1) > 9:
             documents_month = str(num + 1)

        documents.append(dic_documents[documents_month])


    return documents


if __name__ == '__main__':
    hotel_code = input("ホテルコード : ")
    month = input("分析月(1, 2 ~ 10, 11, 12) : ")

    documents = make_doc(hotel_code)#ホテルコードとmonthを関数に渡す

    # gensim用に成形
    texts = list(map(lambda x:x.split(),documents))

    print('===単語->idの変換辞書===')
    dictionary = corpora.Dictionary(texts)

    # textsをcorpus化
    print('===corpus化されたtexts===')
    corpus = list(map(dictionary.doc2bow,texts))

    test_model = models.TfidfModel(corpus,normalize=False) # デフォルトでは normalize=True



    # corpusへのモデル適用
    corpus_tfidf = test_model[corpus]

    # 表示
    print('===結果表示===')
    i = 0
    for doc in corpus_tfidf:
        i = i + 1
        if i > 2:
            break
        print(doc)






#
