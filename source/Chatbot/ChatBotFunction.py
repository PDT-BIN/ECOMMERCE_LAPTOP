from controls.models import LaptopModel
import spacy


def findLaptop(inp, context):
    nlp_laptop = spacy.load("Chatbot/trained_model")
    doc_laptop = nlp_laptop(inp)
    laptops = []
    foundLaptop = False
    for entity in doc_laptop.ents:
        if entity.label_ == "LAPTOP":
            foundLaptop = True
            laptopsQuery = LaptopModel.objects.filter(quantity__gt=0)
            for laptop in laptopsQuery:
                if f'{laptop.name} - {laptop.specification.id}'.lower().find(entity.text.lower()) != -1:
                    laptops.append(laptop)
    if foundLaptop == False and len(context) > 0:
        for laptopCont in context:
            laptopsQuery = LaptopModel.objects.filter(quantity__gt=0)
            for laptop in laptopsQuery:
                if f'{laptop.name} - {laptop.specification.id}'.lower().find(laptopCont.lower()) != -1:
                    laptops.append(laptop)
    return laptops[:5]


def LaptopLinkAsking(inp, context):
    images = []
    ids = []
    specs = []
    name = []
    laptops = findLaptop(inp, context)
    for laptop in laptops:
        images.append(laptop.image.url)
        ids.append(laptop.id)
        specs.append(laptop.specification.id)
        name.append(laptop.name)
    return images, ids, specs, name


def LaptopSpecsAsking(inp, context):
    laptops = findLaptop(inp, context)
    specs = []
    name = []
    for i in range(len(laptops)):
        name.append(laptops[i].name + " - " + str(laptops[i].specification.id))
        specs.append("\n"+str(i+1)+". "+str(laptops[i].name)
                     + " - Mã thông số kĩ thuật: " +
                     str(laptops[i].specification.id) +
                     "\n- Hệ điều hành: " + str(laptops[i].specification.os)
                     + "\n- Ram: " +
                     str(laptops[i].specification.ram) +
                     "\n- CPU: "+str(laptops[i].specification.cpu)
                     + "\n- Ổ đĩa: "+str(laptops[i].specification.disk) +
                     "\n- Card đồ họa: " + str(laptops[i].specification.vga)
                     + "\n- Pin: "+str(laptops[i].specification.battery)+" giờ"+"\n- Màn hình: " + str(
                         laptops[i].specification.screensize)+'" - '+str(laptops[i].specification.resolution)
                     + "\n- Trọng lượng: "+str(laptops[i].specification.weight))
    return specs, name


def LaptopPriceAsking(inp, context):
    laptops = findLaptop(inp, context)
    specs = []
    name = []
    for i in range(len(laptops)):
        name.append(laptops[i].name + " - " + str(laptops[i].specification.id))
        specs.append(str(i+1)+". "+str(laptops[i].name)
                     + " - Mã thông số kĩ thuật: "+str(laptops[i].specification.id)+"\n+ Giá: " + str(laptops[i].price))
    return specs, name


def LaptopOSAsking(inp, context):
    laptops = findLaptop(inp, context)
    specs = []
    name = []
    for i in range(len(laptops)):
        name.append(laptops[i].name + " - " + str(laptops[i].specification.id))
        specs.append(str(i+1)+". "+str(laptops[i].name)
                     + " - Mã thông số kĩ thuật: "+str(laptops[i].specification.id)+"\n+ Hệ điều hành: " + str(laptops[i].specification.os))
    return specs, name
