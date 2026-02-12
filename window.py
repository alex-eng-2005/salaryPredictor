from PySide6.QtWidgets import *
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.mainScreen()
    
    #Creates the main screen
    def mainScreen(self):
        #HBox
        h_box = QHBoxLayout()
        self.my_gender = QComboBox()
        self.my_education = QComboBox()
        self.my_job = QComboBox()
        self.my_age = QLineEdit()
        self.my_experience = QLineEdit()
        self.enter = QPushButton("Enter")
        self.validAge = False
        self.valid_experience = False
        
        #Set the title
        self.setWindowTitle("Salary Prediction")
        width = self.getScreenWidthHeight()[0]
        height = self.getScreenWidthHeight()[1]
        
        #Sets up the df
        self.df = pd.read_csv("Salary Data.csv")
        self.df = self.df.dropna()
        
        #Sets up the gender, education, and job title
        gender = list(set([x[1] for x in self.df[["Gender"]].itertuples()]))
        education = list(set([x[1] for x in self.df[["Education Level"]].itertuples()]))
        jobTitle = sorted(list(set([x[1] for x in self.df[["Job Title"]].itertuples()])))
        
        #Edits my Message
        self.my_age.setPlaceholderText("Enter age")
        self.my_age.textChanged.connect(lambda value: self.isNumber(value, 0))
        self.my_gender.addItems(gender)
        self.my_education.addItems(education)
        self.my_job.addItems(jobTitle)
        self.my_experience.setPlaceholderText("Enter Number of Experience")
        self.my_experience.textChanged.connect(lambda value: self.isNumber(value, 1))
        self.enter.clicked.connect(self.enterResults)
        
        #Adds the buttons
        h_box.addWidget(self.my_age)
        h_box.addWidget(self.my_gender)
        h_box.addWidget(self.my_education)
        h_box.addWidget(self.my_job)
        h_box.addWidget(self.my_experience)
        h_box.addWidget(self.enter)
        
        #Puts the window in the middle of your screen
        self.setGeometry(width / 4 + 100, height / 4, width / 2, height / 2)
        self.setLayout(h_box)
        #self.createModel(df)
        #self.createModel(self.df, [1,2,3,4,5,6])

    #Gets Valid number
    def isNumber(self, value, index):
        #Test 
        try:
            test = int(value)
            if test < 0:
                raise Exception()
            #Checks if we are typing on index 1
            if index == 0:
                self.validAge = True
            else:
                self.valid_experience = True
                
        #Exception
        except Exception:
            if index == 0:
                self.validAge = False
            else:
                self.valid_experience = False
                
    #Gets the screen and the height of the main screen
    def getScreenWidthHeight(self):
        main_screen = QGuiApplication.primaryScreen()
        width = main_screen.size().width()
        height = main_screen.size().height()
        return [width, height]
    
    #Enter in your results
    def enterResults(self):
        #Checks if you have any valid values
        if self.validAge and self.valid_experience:
            age = self.my_age.text()
            gender = self.my_gender.currentText()
            education_level = self.my_education.currentText()
            title = self.my_job.currentText()
            experience = self.my_experience.text()

            #Your results
            results = [age, gender, education_level, title, experience]
            #Creates the model
            getPay = self.createModel(self.df, results)
            QMessageBox.about(self, "Your Pay", f"Your pay is ${float(getPay):,.2f}")
            
    #The model itself
    def createModel(self, df, results):
        X = df[["Age","Gender","Education Level","Job Title","Years of Experience"]].values
        y = df["Salary"]
        le = LabelEncoder()
        my_map = {}
        counter = 0
        
        #For loop for the values
        for i in range(len(X[0])):
            #Checks if we are on the on either the gender, education level, job title, and years of experience
            if counter > 0 and counter < 4:
                #Gets a copy
                XCopy = [x for x in X[:,i]]
                #Transforms
                X[:,i] = le.fit_transform(X[:,i])
                #Loops around the X array
                for z in range(len(X[:,i])):
                    #Edit the map
                    my_map[XCopy[z]] = X[:,i][z]
            #Adds one
            counter += 1
        
        #Splits the test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        #Creates model
        model = RandomForestRegressor(n_estimators=500, min_samples_split=2, max_depth=500, random_state=42)
        #Trains the model
        model.fit(X_train, y_train)
        for i in range(1, len(results) - 1):
            results[i] = my_map[results[i]]
        #Gets the results
        result = model.predict([results])
    
        return result
        #Returns the result
        #return result
        #print("R^2", model.score(X_test, y_test))
		
  
			
       
        
        
        
        
    


        


