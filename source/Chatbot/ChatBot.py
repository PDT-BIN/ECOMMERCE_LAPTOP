from googletrans import Translator
import pickle
import json
import random
import tflearn
import numpy as np
import spacy
import csv
from Chatbot import ChatBotFunction

import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()


# DOWNLOAD ONLY ONCE.
# nltk.download('punkt')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')


with open("Chatbot/intents.json") as file:
    data = json.load(file)

try:
    # rb là read-byte vì ta sẽ lưu dưới dạng byte.
    with open("Chatbot/trained.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y = []
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
        if intent["tag"] not in labels:
            labels.append(intent["tag"])
    banned_words = ["?", "!", ",", "."]
    words = [stemmer.stem(w.lower()) for w in words if w not in banned_words]
    words = sorted(list(set(words)))
    labels = sorted(labels)
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]
    for x, doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w.lower()) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)
    training = np.array(training)
    output = np.array(output)
    with open("Chatbot/trained.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

# Chiều dài của dữ liệu đều như nhau
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)  # kết nối mạng neuron đầu tiên có 8 node
net = tflearn.fully_connected(net, 8)  # kết nối mạng neuron thứ 2 có 8 node
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("Chatbot/model.tflearn")
except:
    model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
    model.save("Chatbot/model.tflearn")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def word_to_num(ordinal_word):
    words = ordinal_word.lower().split()
    if "first" in words:
        return 1
    elif "second" in words:
        return 2
    elif "third" in words:
        return 3
    elif "fourth" in words:
        return 4
    elif "fifth" in words:
        return 5
    # Add more cases for additional ordinals as needed
    else:
        return None


def chat(inp: str, context: str):
    inp = inp.replace("?", "").replace(
        "!", "").replace(",", "").replace(".", "")
    translator = Translator()
    inp = translator.translate(inp).text
    inp = inp.replace("laptops", "").replace("Laptops", "").replace(
        "laptop", "").replace("Laptop", "").replace("'s", "").strip()
    while "  " in inp:
        inp = inp.replace("  ", " ")
    results = model.predict([bag_of_words(inp, words)])
    results_index = np.argmax(results)

    tag = labels[results_index]

    nlp_laptop = spacy.load("Chatbot/trained_model")
    doc_laptop = nlp_laptop(inp)
    laptops = []
    foundLaptop = False
    for entity in doc_laptop.ents:
        if entity.label_ == "LAPTOP":
            foundLaptop = True

    if foundLaptop:
        results = [u if 7 <= i <= 9 or 15 <= i <= 16 or i ==
                   13 else 0 for i, u in enumerate(results[0])]
        results_index = np.argmax(results)
        # if results[0][results_index] < 0.7:
        #     f = open('Chatbot/record/misunderstand.csv', 'a', newline='')
        #     csvwt = csv.writer(f)
        #     csvwt.writerow([inp])
        #     f.close()
        #     return "Xin lỗi tôi chưa đủ thông minh để hiểu câu vừa rồi", 0, "", ""
        tag = labels[results_index]
        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                if tag == "LaptopAsking":
                    laptops = ChatBotFunction.LaptopLinkAsking(inp, context)
                    if len(laptops[0]) == 0:
                        return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                    else:
                        context = []
                        for i in range(len(laptops[0])):
                            context.append(
                                str(laptops[3][i])+" - "+str(laptops[2][i]))
                    return translator.translate(random.choice(responses).replace("<amount>", str(len(laptops[0]))), dest='vi').text, laptops, context, tag

                if tag == "LaptopSpecsAsking":
                    specs = ChatBotFunction.LaptopSpecsAsking(inp, context)
                    if len(specs[0]) == 0:
                        return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                    else:
                        context = []
                        for i in range(len(specs[0])):
                            context.append(specs[1][i])
                    ans = translator.translate(
                        random.choice(responses), dest='vi').text
                    for spec in specs[0]:
                        ans += "\n"+spec
                    return ans, 0, context, tag

                if tag == "IsLaptopAvailable":
                    laptops = ChatBotFunction.LaptopLinkAsking(inp, context)
                    if len(laptops[0]) == 0:
                        return translator.translate(random.choice(responses[1]).replace("<amount>", str(len(laptops[0]))), dest='vi').text, 0, context, tag
                    else:
                        context = []
                        for i in range(len(laptops[0])):
                            context.append(
                                str(laptops[3][i])+" - "+str(laptops[2][i]))
                        return translator.translate(random.choice(responses[0]).replace("<amount>", str(len(laptops[0]))), dest='vi').text, laptops, context, tag

                if tag == "LaptopAskingSpecific":
                    return translator.translate(random.choice(responses), dest='vi').text, 0, context, tag

                if tag == "LaptopPriceAsking":
                    specs = ChatBotFunction.LaptopPriceAsking(inp, context)
                    if len(specs[0]) == 0:
                        return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                    else:
                        context = []
                        for i in range(len(specs[0])):
                            context.append(specs[1][i])
                    ans = translator.translate(
                        random.choice(responses), dest='vi').text
                    for spec in specs[0]:
                        ans += "\n"+spec
                    return spec, 0, context, tag

                if tag == "LaptopOSAsking":
                    specs = ChatBotFunction.LaptopOSAsking(inp, context)
                    if len(specs[0]) == 0:
                        return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                    else:
                        context = []
                        for i in range(len(specs[0])):
                            context.append(specs[1][i])
                    ans = translator.translate(
                        random.choice(responses), dest='vi').text
                    for spec in specs[0]:
                        ans += "\n"+spec
                    return ans, 0, context, tag
                return translator.translate(random.choice(responses), dest='vi').text, 0, "", tag
        f = open('Chatbot/record/misunderstand.csv', 'a', newline='')
        csvwt = csv.writer(f)
        csvwt.writerow([inp])
        f.close()
        return "Xin lỗi tôi chưa đủ thông minh để hiểu câu vừa rồi", 0, "", ""

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(inp)
    newContext = []
    for entity in doc.ents:
        if entity.label_ == "ORDINAL":
            try:
                newContext.append(context[word_to_num(entity.text)-1])
            except:
                return "Xin lỗi tôi không hiểu, bạn vui lòng nhập lại", 0, "", ""
        if entity.label_ == "CARDINAL":
            for laptop in context:
                if laptop.find(entity.text):
                    newContext.append(laptop)
    if len(newContext) > 0:
        context = newContext

    brand = ["hp", "asus", "acer", "lenovo", "samsung",
             "chuwi", "msi", "dell", "lg", "gigabyte",
             "clevo", "vaio", "tongfang", "xiaomi",
             "microsoft", "corsair", "getac", "dynabook",
             "apple", "razer", "bmorn", "huawei"]
    for word in inp.split(" "):
        if word.lower() in brand:
            return "Đây là đường link đến hãng mà bạn cần tìm", "http://127.0.0.1:8000/?kw="+str(word.capitalize()), "", "LaptopBrand"

    if results[0][results_index] < 0.7:
        f = open('Chatbot/record/misunderstand.csv', 'a', newline='')
        csvwt = csv.writer(f)
        csvwt.writerow([inp])
        f.close()
        return "Xin lỗi tôi chưa đủ thông minh để hiểu câu vừa rồi", 0, "", ""

    for tg in data["intents"]:
        if tg['tag'] == tag:
            responses = tg['responses']
            if tag == "LaptopAsking":
                laptops = ChatBotFunction.LaptopLinkAsking(inp, context)
                if len(laptops[0]) == 0:
                    return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                else:
                    context = []
                    for i in range(len(laptops[0])):
                        context.append(
                            str(laptops[3][i])+" - "+str(laptops[2][i]))
                return translator.translate(random.choice(responses).replace("<amount>", str(len(laptops[0]))), dest='vi').text, laptops, context, tag

            if tag == "LaptopSpecsAsking":
                specs = ChatBotFunction.LaptopSpecsAsking(inp, context)
                if len(specs[0]) == 0:
                    return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                else:
                    context = []
                    for i in range(len(specs[0])):
                        context.append(specs[1][i])
                ans = translator.translate(
                    random.choice(responses), dest='vi').text
                for spec in specs[0]:
                    ans += "\n"+spec
                return ans, 0, context, tag

            if tag == "IsLaptopAvailable":
                laptops = ChatBotFunction.LaptopLinkAsking(inp, context)
                if len(laptops[0]) == 0:
                    return translator.translate(random.choice(responses[1]).replace("<amount>", str(len(laptops[0]))), dest='vi').text, 0, context, tag
                else:
                    context = []
                    for i in range(len(laptops[0])):
                        context.append(
                            str(laptops[3][i])+" - "+str(laptops[2][i]))
                    return translator.translate(random.choice(responses[0]).replace("<amount>", str(len(laptops[0]))), dest='vi').text, laptops, context, tag

            if tag == "LaptopAskingSpecific":
                return translator.translate(random.choice(responses), dest='vi').text, 0, context, tag

            if tag == "LaptopPriceAsking":
                specs = ChatBotFunction.LaptopPriceAsking(inp, context)
                if len(specs[0]) == 0:
                    return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                else:
                    context = []
                    for i in range(len(specs[0])):
                        context.append(specs[1][i])
                ans = translator.translate(
                    random.choice(responses), dest='vi').text
                for spec in specs[0]:
                    ans += "\n"+spec
                return spec, 0, context, tag

            if tag == "LaptopOSAsking":
                specs = ChatBotFunction.LaptopOSAsking(inp, context)
                if len(specs[0]) == 0:
                    return "Xin lỗi shop chúng tôi không bán sản phẩm đó", 0, "", tag
                else:
                    context = []
                    for i in range(len(specs[0])):
                        context.append(specs[1][i])
                ans = translator.translate(
                    random.choice(responses), dest='vi').text
                for spec in specs[0]:
                    ans += "\n"+spec
                return ans, 0, context, tag

            if tag == "LaptopOffice":
                return translator.translate(random.choice(responses), dest='vi').text, "http://127.0.0.1:8000/?kw=V%C4%83n%20ph%C3%B2ng", "", tag

            if tag == "LaptopLight":
                return translator.translate(random.choice(responses), dest='vi').text, "http://127.0.0.1:8000/?kw=M%E1%BB%8Fng%20nh%E1%BA%B9", "", tag

            if tag == "LaptopGaming":
                return translator.translate(random.choice(responses), dest='vi').text, "http://127.0.0.1:8000/?kw=Gaming", "", tag

            if tag == "LaptopGraphic":
                return translator.translate(random.choice(responses), dest='vi').text, "http://127.0.0.1:8000/?kw=%C4%90%E1%BB%93%20h%E1%BB%8Da%20-%20K%E1%BB%B9%20thu%E1%BA%ADt", "", tag

            return translator.translate(random.choice(responses), dest='vi').text, 0, "", tag
    f = open('Chatbot/record/misunderstand.csv', 'a', newline='')
    csvwt = csv.writer(f)
    csvwt.writerow([inp])
    f.close()
    return "Xin lỗi tôi chưa đủ thông minh để hiểu câu vừa rồi", 0, "", ""
