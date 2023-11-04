import joblib
from sklearn.feature_extraction.text import CountVectorizer
from .models import LaptopModel


VERCTORIZE = CountVectorizer()
VERCTORIZE = joblib.load(r'controls\model_files\vectorize_transform.pkl')
LOADED_MODEL = joblib.load(r'controls\model_files\model_label.pkl')


def make_predict(laptop_model: LaptopModel) -> str:
    # STANDARD.
    name = laptop_model.name.replace(" ", "_")
    screen = f'{laptop_model.specification.screensize} {laptop_model.specification.resolution}'
    cpu = laptop_model.specification.cpu
    cpu = cpu.replace(' ', '_', len(cpu.split(" ")) - 2)
    vga = laptop_model.specification.vga
    ram = laptop_model.specification.ram
    disk = laptop_model.specification.disk.replace(" GB - ", "_GB ")
    weight = laptop_model.specification.weight
    os = laptop_model.specification.os
    battery = laptop_model.specification.battery
    # SUMMARY.
    features = " ".join([str(name), str(screen), str(cpu), str(vga), str(ram),
                        str(disk), str(weight), str(os), str(battery)])
    label_vector = VERCTORIZE.transform([features])
    # PREDICT.
    return LOADED_MODEL.predict(label_vector)[0]
