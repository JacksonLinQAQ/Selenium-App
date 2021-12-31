from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from selenium import webdriver
import random
import requests
import shutil

class App():
    def __init__(self):
        uifile = QFile("main_zh.ui")
        uifile.open(QFile.ReadOnly)
        uifile.close()

        self.ui = QUiLoader().load(uifile)
        self.ui.gettext.clicked.connect(self.gettext)
        self.ui.getimg.clicked.connect(self.getimg)
    
    def gettext(self):
        self.ui.output.setText("")
        self.getmethod = self.ui.method.currentText()
        self.geturl = self.ui.url.text()
        self.gettarget = self.ui.findtarget.text()
        self.data = ""

        try:
            path = "chromedriver.exe"
            driver = webdriver.Chrome(path)
            print("Get ChromeDriver Success")
            driver.get(self.geturl)
            print("Get URL Success")
            if self.getmethod == "ID":
                self.data = driver.find_element_by_id(self.gettarget).text
                print("Getting Text From ID")
            elif self.getmethod == "Class":
                self.data = driver.find_element_by_class_name(self.gettarget).text
                print("Getting Text From Class")
            elif self.getmethod == "CSS Selector":
                self.data = driver.find_element_by_css_selector(self.gettarget).text
                print("Getting Text From CSS Selector")
            elif self.getmethod == "Name":
                self.data = driver.find_element_by_name(self.gettarget).text
                print("Getting Text From Name")

            self.ui.output.setText(self.data)
            print("Get Text Success")
            
            driver.quit()
            self.save()

        except Exception as exc:
            self.ui.output.setText(str(exc))
            #self.ui.output.setText("Error: Something happened! Please comfirm anything correct: \n1) Please Check ChromeDriver Has Been Installed And In A Correct PATH\n2) Please Check Your Chrome Version Whether Chrome 96\n3) Please Check Your URL and Target Whether Correct")
            driver.quit()
        

    def save(self):
        self.data = self.ui.output.toPlainText()
        self.randint = random.randint(100, 999)
        with open(f"Texts/text{self.randint}.txt", mode="w", encoding="utf-8") as txt:
            txt.write(self.data)
        print(f"Save Text As text{self.randint}.txt")
        QMessageBox.about(self.ui, "Save Text Success", f"Save Text Success\nFile Name: text{self.randint}.txt")
    
    def getimg(self):
        reply = QMessageBox.question(self.ui, "Warning", "This Process Will Get All Images From This Website\nAre You Sure To Continue?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.getmethod = self.ui.method.currentText()
            self.geturl = self.ui.url.text()
            self.gettarget = self.ui.findtarget.text()
            self.data = ""
            self.success = 0
            self.fail = 0
            self.total = 0

            try:
                path = "chromedriver.exe"
                driver = webdriver.Chrome(path)
                print("Get ChromeDriver Success")
                driver.get(self.geturl)
                print("Get URL Success")

                images = driver.find_elements_by_tag_name('img')
                for image in images:
                    self.randint = random.randint(100, 999)
                    
                    res = requests.get(image.get_attribute('src'), stream = True)
                    if res.status_code == 200:
                        with open(f"Images/img{self.randint}.jpg",'wb') as f:
                            shutil.copyfileobj(res.raw, f) 
                        self.success += 1
                        self.total += 1
                        print("An Image Downloaded Sucessfully")
                    else:
                        self.fail += 1
                        self.total += 1
                        print("An Image Download Fail")

                print(f"Images Saved\nTotal: {self.total}\nSuccess: {self.success}\nFail: {self.fail}")
                driver.quit()
                QMessageBox.about(self.ui, "Save Image", f"Images Saved\nTotal: {self.total}\nSuccess: {self.success}\nFail: {self.fail}")

            except Exception as exc:
                self.ui.output.setText(str(exc))
                driver.quit()
        
app = QApplication([])

win = App()
win.ui.show()
app.exec_()