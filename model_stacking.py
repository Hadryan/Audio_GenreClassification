import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC,NuSVC
from vecstack import stacking
from xgboost import XGBClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score



train = pd.read_csv('df_features.csv')
data_list = list(train.columns)
genre_list = train.iloc[:, -1]
encoder = LabelEncoder()
y = encoder.fit_transform(genre_list)
scaler = StandardScaler()

x = scaler.fit_transform(np.array(train.iloc[:, :-1], dtype=float))
X_train, X_test, Y_train, Y_test = train_test_split(x, y, test_size=0.20, random_state=2020, stratify=y)


classifier1=SVC(C=50, degree=1, gamma="auto",kernel="rbf",probability=False,decision_function_shape="ovr")
classifier2=RandomForestClassifier()
classifier3=LogisticRegression(random_state=0, solver='lbfgs', max_iter=1000,multi_class='multinomial')
classifier4=XGBClassifier(random_state=0, n_jobs=-1, learning_rate=0.1, n_estimators=100, max_depth=3)
classifier5=NuSVC(degree=1,kernel="rbf",nu=0.25,probability=False)
classifier6=KNeighborsClassifier(n_neighbors=5,n_jobs=-1)
models=[classifier1, classifier2, classifier3, classifier4,  classifier5, classifier6]
S_train, S_test= stacking(models, X_train, Y_train, X_test, regression=False, mode='oof_pred_bag', needs_proba=False,
                          save_dir=None,metric=accuracy_score,n_folds=5,stratified=True,shuffle=True,random_state=0,
                          verbose=2)
model=XGBClassifier(random_state=0, n_jobs=-1, learning_rate=0.1, n_estimators=100, max_depth=3)
model=model.fit(S_train, Y_train)
y_pred=model.predict(S_test)
print('Final prediction score: [%.8f]'%accuracy_score(Y_test,y_pred))