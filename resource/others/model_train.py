from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import joblib
# Tắt cảnh báo lỗi khi sửa dữ liệu trong pd
pd.options.mode.chained_assignment = None
# Đọc tệp CSV và lưu dữ liệu vào một DataFrame
df = pd.read_csv("dataSum.csv", encoding='utf-8', sep=';')
df = df.drop(columns=['Img', 'Price'])
data_df_x = df.iloc[:, :9]
data_df_y = df.iloc[:, 9:]
data_df_x = data_df_x.dropna()
data_df_y = data_df_y.dropna()
# print(data_df_x)
for i in range(len(data_df_x["Weight"])):
    a = data_df_x["Weight"][i].replace(' Kg', '')
    data_df_x["Weight"][i] = a.strip()
for i in range(len(data_df_x["SSD"])):
    a = data_df_x["SSD"][i].replace(' GB - ', '_GB ')
    data_df_x["SSD"][i] = a
for i in range(len(data_df_x["Screen"])):
    a = data_df_x["Screen"][i].replace('" - ', ' ')
    data_df_x["Screen"][i] = a
for i in range(len(data_df_x["CPU"])):
    numOspace = len(data_df_x["CPU"][i].split(" "))
    numOreplace = 0
    if numOspace > 2:
        numOreplace = numOspace - 2
    a = data_df_x["CPU"][i].replace(' ', '_', numOreplace)
    data_df_x["CPU"][i] = a
for i in range(len(data_df_x["Name"])):
    a = data_df_x["Name"][i].replace(' ', '_')
    data_df_x["Name"][i] = a
# for i in range(len(data_df_x["Battery"])):
#      # if data_df_x["Battery"][i].dtype ==
#      a = str(data_df_x["Battery"][i])
#      data_df_x["Battery"][i] = a
data_df_x['Battery'] = data_df_x['Battery'].astype(str)
data_x_raw = data_df_x.values
data_y = data_df_y.values
# print(data_x_raw)
#######
# X = [['rog', 'i5', 'rtx 3090'], ['asus vivobook', 'i5', 'intel iris xe'], ['dell workstation', 'i9', 'rtx quadro 3000'], ['surface', 'i3', 'intel iris xe']]
# y = np.array(['Gaming', 'Văn phòng', 'Kỹ thuật, đồ hoạ', 'Mỏng nhẹ'])
##########
# for x in data_x:
#      for i in range(len(x)):
#           a = x[i].replace(" ", "_")
#           x[i] = a
#           i = i + 1
############
data_x = []
for x in data_x_raw:
    a = " ".join(x)
    data_x.append(a)
##############
# vectorizer = CountVectorizer()
# data_x_vectorize = vectorizer.fit_transform(data_x)
# joblib.dump(vectorizer, 'vectorize_transform.pkl')
# train_y = data_y.ravel()
# x_train, x_test, y_train, y_test = train_test_split(data_x_vectorize, data_y, test_size=0.25, random_state=42)
# clf = make_pipeline(StandardScaler(with_mean=False), SVC(gamma='auto'))
# Load
clf = joblib.load('model_label.pkl')
vectorizer = joblib.load('vectorize_transform.pkl')
######
# clf.fit(data_x_vectorize, train_y)
# joblib.dump(clf, 'model_label.pkl')
# accuracy = clf.score(x_test, y_test)
# print("Độ chính xác dùng tập kiểm tra: ", accuracy)
######
test = ['Asus_Vivobook_Flip', '14.0 1920x1200', 'INTEL_Celeron N4020',
        'INTEL HD Graphics 600', '4 GB DDR4', '128_GB EMMC', '1.3', 'Windows 10 home', '10']
test = [" ".join(test)]
test_tran = vectorizer.transform(test)
test_1 = clf.predict(test_tran)
print(test_1)
############
# pred_test = clf.predict(x_test)
# # print(pred_test)
# report = classification_report(y_test, pred_test)
# print("Đánh giá bằng classification_report: \n", report)
