from spacy.training.example import Example
import spacy
import random


def init_data():
    from csv import reader
    with open(r'C:/Users/THAIHOANG/Desktop/Chatbot/trained_model/data.csv') as csv_file:
        sentences = [
            'I would like to buy KEY laptop',
            'Let show me KEY',
            'I wanna buy KEY',
            'What is laptop KEY?',
            'How about laptop KEY?',
            'Do you have laptop KEY?',
            'Tell me about laptop KEY',
            'Could you show me laptop KEY?',
            'Show me KEY',
            'Is laptop KEY available?',
            'I need information about model KEY',
            'Could you give me some information of laptop KEY?',
            'I want a new laptop KEY',
            'I need a laptop KEY',
            'Is model KEY new?',
            'Hello! I need a old laptop KEY',
            'Show me information about model KEY',
            'Is model KEY available in your shop?'
        ]
        results = []
        for i, data in enumerate(reader(csv_file)):
            if i > 318:
                break
            name = data[0].removesuffix('(US)')
            for sentence in sentences:
                question = sentence.replace('KEY', name)
                index = question.index(name)
                position = index, index + len(name)
                results.append(
                    (question, {"entities": [(position[0], position[1], "LAPTOP")]}))
    return (results)


annotated_data = [
    ("I bought a new MacBook Pro yesterday.",
     {"entities": [(15, 26, "LAPTOP")]}),
    ("The Dell XPS is a powerful laptop.", {"entities": [(4, 12, "LAPTOP")]}),
    ("I really like HP Chromebook 14", {"entities": [(14, 30, "LAPTOP")]}),
    ("What are you going to do with that Asus VivoBook E410",
     {"entities": [(35, 53, "LAPTOP")]}),
    ("He is buying a Acer Chromebook 14", {"entities": [(15, 33, "LAPTOP")]}),
    ("How much is a Asus Chromebook 14", {"entities": [(14, 32, "LAPTOP")]}),
    ("Do you like HP 14z?", {"entities": [(12, 18, "LAPTOP")]}),
    ("Asus VivoBook L410 is really good", {"entities": [(0, 18, "LAPTOP")]}),
    ("Lenovo IdeaPad 1-14 is a beast", {"entities": [(0, 19, "LAPTOP")]}),
    ("I hate Lenovo IdeaPad 1-15", {"entities": [(7, 26, "LAPTOP")]}),
    ("He loves Lenovo IdeaPad 3 Chromebook 14",
     {"entities": [(9, 39, "LAPTOP")]}),
    ("Samsung Chromebook 4 XE350 is a family laptop",
     {"entities": [(0, 26, "LAPTOP")]}),
    ("You can't beat a Lenovo IdeaPad 3 CB 14",
     {"entities": [(17, 39, "LAPTOP")]}),
    ("How strong is HP Chromebook 14at?", {"entities": [(14, 32, "LAPTOP")]}),
    ("She is using a HP Chromebook x360 14a",
     {"entities": [(15, 37, "LAPTOP")]}),
    ("Lenovo IdeaPad Flex 5 14 is her laptop",
     {"entities": [(0, 25, "LAPTOP")]}),
    ("Can you hate a Chuwi  GemiBook X?", {"entities": [(15, 32, "LAPTOP")]}),
    ("MSI Gaming Katana GF66 is my laptop", {"entities": [(0, 22, "LAPTOP")]}),
    ("What is a Dell Gaming G15 doing here?",
     {"entities": [(10, 25, "LAPTOP")]}),
    ("They use a MSI Gaming GF63", {"entities": [(11, 26, "LAPTOP")]}),
    ("She dislikes Dell Inspiron 16", {"entities": [(13, 29, "LAPTOP")]}),
    ("I'd like to buy LG gram 14", {"entities": [(16, 26, "LAPTOP")]}),
    ("Lenovo IdeaPad Flex 5 15 is what I'd like to buy", {"entities": [(0, 25, "LAPTOP")]}),
    ("Lenovo Slim 7 14 is nice", {"entities": [(0, 16, "LAPTOP")]}),
    ("I want to buy Acer Predator Helios 300 15", {"entities": [(14, 41, "LAPTOP")]}),
    ("Show me Asus VivoBook Pro 16X M7600", {"entities": [(8, 35, "LAPTOP")]}),
    ("Asus VivoBook Pro 16 OLED is my favorite",
     {"entities": [(0, 25, "LAPTOP")]}),
    ("Asus ZenBook 14X OLED UX5400 is a good laptop",
     {"entities": [(0, 28, "LAPTOP")]}),
    ("alo, hello hui, Asus ZenBook Pro 16X OLED UX7602 good, nice, superb",
     {"entities": [(16, 48, "LAPTOP")]}),
    ("how what, surf Microsoft Surface Laptop 5 15 amazing, wow, crazy",
     {"entities": [(15, 44, "LAPTOP")]}),
    ("What an amazing Acer TravelMate P2 TMP214-41 laptop",
     {"entities": [(16, 44, "LAPTOP")]}),
    ("What is Lenovo IdeaPad S145-15?", {"entities": [(8, 30, "LAPTOP")]}),
    ("Lenovo ThinkBook 14s Yoga G3 is my jam",
     {"entities": [(0, 28, "LAPTOP")]}),
    ("The Acer TravelMate P4 TMP416 is a reliable business laptop with a sleek design and powerful performance", {
     "entities": [(4, 43, "LAPTOP")]}),
    ("The Asus ZenBook 14X OLED UX5400 combines stunning visuals with impressive processing power, making it a top choice for multimedia enthusiasts.", {
     "entities": [(4, 68, "LAPTOP")]}),
]+init_data()


# Create a blank English model
nlp = spacy.blank("en")

# Add Named Entity Recognition (NER) component to the pipeline
ner = nlp.add_pipe("ner")

# #Convert to spaCy format
# spacy_annotated_data = []
# for text, annotations in annotated_data:
#     entities = annotations["entities"]
#     example = Example.from_dict(nlp.make_doc(text), {"entities": entities})
#     spacy_annotated_data.append(example)

# # Update the model with training data
# nlp.begin_training()
# for epoch in range(10):  # You can adjust the number of epochs
#     random.shuffle(spacy_annotated_data)
#     for example in spacy_annotated_data:
#         nlp.update([example], drop=0.5, losses={})

# Save the trained model
output_dir = "trained_model"
# nlp.to_disk(output_dir)

# Load the trained model
loaded_nlp = spacy.load(output_dir)

# Test the model

# from csv import reader
# with open(r'C:/Users/THAIHOANG/Desktop/Chatbot/trained_model/data.csv') as csv_file:
#     for i, data in enumerate(reader(csv_file)):
#             if i > 318:
#                 name = data[0].removesuffix(' (US)').strip()
#                 test_text = f"Hello show me infomation about {data[0]}. THank you very much"
#                 doc = loaded_nlp(test_text)
#                 for ent in doc.ents:
#                     if ent.text!=data[0]:
#                         print(ent.text, data[0], ent.text==data[0])
test_text = "hello world Im Andrew and I'd like to buy a Asus 123 XYZ"
doc = loaded_nlp(test_text)
for ent in doc.ents:
    print(ent.text, ent.label_)
