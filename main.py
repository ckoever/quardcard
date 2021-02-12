from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import os
import sys
import random
import base64
import playsound

SETTINGS_STYLESHEET="Dark Mode"
SETTINGS_STYLE="Fusion"
SETTINGS_COLORMODE="colorful"
SETTINGS_MAXSIZE="disable"

try:
    LOCAL_FILE=open("SETTINGS.txt")
    SETTINGS_STYLESHEET=LOCAL_FILE.readline()
    SETTINGS_STYLE=LOCAL_FILE.readline()
    SETTINGS_COLORMODE=LOCAL_FILE.readline()
    SETTINGS_MAXSIZE=LOCAL_FILE.readline()
    LOCAL_FILE.close()
    del LOCAL_FILE
except:
    LOCAL_FILE=open("SETTINGS.txt", "w")
    LOCAL_FILE.write("Dark Mode\nFusion\ncolorful\ndisable")
    LOCAL_FILE.close()
    del LOCAL_FILE

if "Dark Mode" in SETTINGS_STYLESHEET:
    from uidata.MAINWINDOW import *
elif "Light Mode" in SETTINGS_STYLESHEET:
    from uidata.MAINWINDOW_LIGHT import *
from uidata.ABOUT import *
from uidata.CREATOR import *
from uidata.OPTIONS_INDEX_CARD import *
from uidata.LIVE_EDIT import *
from uidata.OPTIONS_QUESTION_ENTRY import *
from uidata.WARNING import *
from uidata.OPTIONS_QUESTION_MULTIPLE_CHOICE import *
from uidata.OPTIONS_QUESTION_RADIO import *
from uidata.OPTIONS_QUESTION_ORDER import *
from uidata.LICENSE_WIZARD import *
from uidata.SETTINGS import *
    
    
LICENCE_AGREED=False


class index_card:
    side = 0
    #0 is back
    #1 is front
    
    #variable to transmit the Datastream
    data=0
    
    #function to write the text on the index card
    def prg(DATA, INDEX):
        #print(DATA)
        
        #store the datastream for the secon function
        index_card.data=DATA
        
        if index_card.side==0:
            
            #flip it to the back
            back_side_text=DATA['SIDE-A']
            ui.index_card_obj_card.setText(back_side_text)
            #set status of card to front
            index_card.side = 1
        #when card is front...
        else:
            #flip it to the back
            front_side_text=DATA['SIDE-B']
            ui.index_card_obj_card.setText(front_side_text)
            #set status of card to back
            index_card.side = 0
            main.event_handler(parameter={"POINTS": -2, "TIME": 5})
    
    
class order:
    #declare variables
    selected_item=[]
    random_order=[]
    solutions=[]
    position=0
    index=0
    
    #function  to order the items
    def prg(DATA, INDEX):
        #the list of the items in the correct order
        
        order.index=INDEX
        ui.question_order.setEnabled(main.ENABLED[order.index])
        
        order.solutions=DATA['Items']
        
        order.position=INDEX
        
        order.random_order=[]
        
        #random list for shufffle
        order.random_order.extend(order.solutions)
        
        #set the question to the question field
        ui.question_order_question.setPlainText(DATA['Question'])

        #shuffle list
        if main.ENABLED[INDEX]==True:
            random.shuffle(order.random_order)
        
        #add random list to the file
        ui.question_order_list.addItems(order.random_order)
        
        #gray out the items
        #if DATA['Active']==False:
           # ui.question_order.setEnabled(0)
       # else:
          #  ui.question_order.setEnabled(1)
    
    
    #determine the last selected item
    def last_selected():
        order.selected_item=ui.question_order_list.selectedItems()[0].text()
        print(order.selected_item)
    
    #function for the down button
    def down():
        #print(order.selected_item)
        #print(order.random_order)
        
        #push the item down when it is possible
        try:
            index=order.random_order.index(order.selected_item)
            order.random_order[index], order.random_order[index+1] = order.random_order[index+1], order.random_order[index]
            ui.question_order_list.clear()
            ui.question_order_list.addItems(order.random_order)
        except:
            pass
    #function for the up button    
    def up():
        #push the item up when it is possible
        try:
            index=order.random_order.index(order.selected_item)
            order.random_order[index], order.random_order[index-1] = order.random_order[index-1], order.random_order[index]
            ui.question_order_list.clear()
            ui.question_order_list.addItems(order.random_order)
        except:
            pass
     
    #test the right order with the user oder    
    def test():
        #length of the list
        length=len(order.solutions)
        points=0
        order.random_order.clear()
        #
        for index in range(ui.question_order_list.count()):
            #
            order.random_order.append((ui.question_order_list.item(index)).text())
        
        #when the items are in correct order
        if order.solutions==order.random_order:
            ui.question_order.setEnabled(0)
            #print(order.solutions)
            #print(order.random_order)
            points=10*length
            #set 30 points
            main.ENABLED[order.index]=False
            ui.question_order.setEnabled(main.ENABLED[order.index])
            LOCAL=ui.lcd_score.text()
            
            main.event_handler(parameter={"POINTS": +20, "TIME": +60})
            
        else:
            #when the order is not correct
            #for check in range(length):
                
                #then it give ten points per right answer
                #if order.solutions[check]==order.random_order[check]:
                    #points=10+points
            
            main.event_handler(parameter={"POINTS": -10, "TIME": -10})
                    
            
        
class multiple_choice:
    #define class variables
    data=[]
    index=[]
    def prg(DATA, INDEX):
        multiple_choice.index=INDEX
        ui.question_muliple_choice.setEnabled(main.ENABLED[multiple_choice.index])
        
        #import multiple choice answer data
        multiple_choice.data=[]
        multiple_choice.data.extend(DATA["Answers"])
        
        #set title
        ui.question_muliple_choice_question.setPlainText(DATA["Question"])
        
        #set visible objs on basis of answer number
        count=0
        for count in range(16):
            objnow=eval("ui.question_muliple_choice_checkbox_"+str(count+1))
            objnow.setHidden(1)
            objnow.setChecked(0)
            
        #set title for objs
        for count in range(len(multiple_choice.data)):
            objnow=eval("ui.question_muliple_choice_checkbox_"+str(count+1))
            objnow.setHidden(0)
            objnow.setText(multiple_choice.data[count][0])
            if main.ENABLED[multiple_choice.index]==0:
                objnow.setChecked(multiple_choice.data[count][1])
        
    #test if true answers are checked
    def test():
        iswrong=False
        for count in range(len(multiple_choice.data)):
            objnow=eval("ui.question_muliple_choice_checkbox_"+str(count+1))
            if objnow.isChecked() == multiple_choice.data[count][1]:
                pass
            else:
                iswrong=True
            
        if iswrong==False:
            main.ENABLED[multiple_choice.index]=False
            ui.question_muliple_choice.setEnabled(main.ENABLED[multiple_choice.index])
            main.event_handler(parameter={"POINTS": +20, "TIME": +60})
            
        
        else:
            main.event_handler(parameter={"POINTS": -10, "TIME": -10})
            
            
            
        
#program for the radio question module
class radio_question:
    #declarate variables
    random_order=[]
    answers=[]
    ordered_answers=[]
    solution=0
    question=""
    index=0
    
    def prg(DATA, index):
        radio_question.index=index
        ui.question_radio.setEnabled(main.ENABLED[radio_question.index])
        
        #store the datat from the Datastream
        radio_question.question=DATA['question']
        radio_question.ordered_answers=DATA['answers']
        radio_question.answers=DATA['right_answer']
        
        #shuffle the answer list
        random.shuffle(radio_question.random_order)

        ui.question_radio_checkbox_question.setPlainText(radio_question.question)
            
        for count in range(0,4):
            obj=eval("ui.question_radio_checkbox_"+str(count+1))
            obj.setChecked(0)
            obj.setHidden(1)
            
        for count in range(len(radio_question.ordered_answers)):
            obj=eval("ui.question_radio_checkbox_"+str(count+1))
            obj.setHidden(0)
            if main.ENABLED[radio_question.index]==False:
                obj.setChecked(radio_question.answers[count])
            obj.setText(radio_question.ordered_answers[count])
    
    #function to test the solution and the user choosen value
    def test():
        #declare variables
        choosen_answer=0
        checked=[]
        
        #check which checkbox is choosen
        for count in range(len(radio_question.answers)):
            if radio_question.answers[count]==1:
                if eval("ui.question_radio_checkbox_"+str(count+1)+".isChecked()")==True:
                    main.ENABLED[radio_question.index]=False 
                    ui.question_radio.setEnabled(main.ENABLED[radio_question.index])
                    main.event_handler(parameter={"POINTS": +20, "TIME": +60})
        
                else:
                    main.event_handler(parameter={"POINTS": -10, "TIME": -10})
            

    
class entry:
    #define class variables
    DATA=[]
    INDEX=[]
    
    #set title and class variables
    def prg(DATA, INDEX):
        entry.DATA=DATA
        entry.INDEX=INDEX
        ui.question_entry.setEnabled(main.ENABLED[entry.INDEX])
        ui.question_entry_question.setPlainText(DATA["Question"])
        if main.ENABLED[entry.INDEX]:
            ui.question_entry_input_field.setPlainText("")
        else:
            ui.question_entry_input_field.setPlainText(DATA["Answer"])
        
    #test if input filed equals answer
    def test():
        if ui.question_entry_input_field.toPlainText()==entry.DATA["Answer"]:
            #if true, deactivate obj            
            main.ENABLED[entry.INDEX]=False
            ui.question_entry.setEnabled(main.ENABLED[entry.INDEX])
            main.event_handler(parameter={"POINTS": +20, "TIME": +60})
            
        
        else:
            main.event_handler(parameter={"POINTS": -10, "TIME": -10})
            
      
      
class create:
    #declarate variables
    project_DATA=[]
    choosen_one=[]
    project_location=False
    new_project=True
    
    #function for the add button
    def btn_add():
        
        #read out which question type is choosen in the combobox
        create.choosen_one=ui.Ui_CREATOR_UI.type_chooser.currentText()
         
        #when Index Card is choosen
        if create.choosen_one=="Index Card":
            #open function open_options
            options_index_card.open_options()
            print(create.choosen_one)
        
        #when QUestion Entry is choosen
        elif create.choosen_one=="Question + Entry":
            #open function open_options
            options_question_entry.open_options()
            print(create.choosen_one)
        
        elif create.choosen_one=="Question + Radio":
            #open function open_options
            options_radio_question.open_options()
        
        elif create.choosen_one=="Question + Multiple Choice":
            #open function open_options
            options_multiple_choice_question.open_options()
            
        elif create.choosen_one=="Question + Order":
            #open function open_options
            options_order_question.open_options()
            
            
            
    #open the qcq file
    def open_file():
        try:
            create.project_location=QtWidgets.QFileDialog.getOpenFileName(ui.Ui_CREATOR_GUI, 'Open file', 'c:\\',"Quardcard Question File (*.qcq)")[0]
            FILE=open(create.project_location,"rb")
            create.project_DATA=eval(base64.b64decode(FILE.read().decode("ascii")))
            FILE.close()
            
            ui.Ui_CREATOR_UI.list.clear()
            
            for element in create.project_DATA:
                try:
                    item = QtWidgets.QListWidgetItem()
                    icon = QtGui.QIcon()
                    if element["TYPE"]=="index_card":
                        icon.addPixmap(QtGui.QPixmap("index_card/index_card.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    elif element["TYPE"]=="radio_question":
                        icon.addPixmap(QtGui.QPixmap("question_radio/question_radio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    elif element["TYPE"]=="multiple_choice":
                        icon.addPixmap(QtGui.QPixmap("question_multiple_choice/question_multiple_choice.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    elif element["TYPE"]=="entry":
                        icon.addPixmap(QtGui.QPixmap("question_entry/question_entry.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    elif element["TYPE"]=="order":
                        icon.addPixmap(QtGui.QPixmap("question_order/question_order.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    else:
                        icon.addPixmap(QtGui.QPixmap("unsupported/warning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    item.setIcon(icon)
                    item.setText(element["NAME"])
                    ui.Ui_CREATOR_UI.list.addItem(item)
                except:
                    ui.Ui_WARNING_GUI.show()
                    ui.Ui_WARNING_UI.body.setText("Broken or unsusable file.")
            
            ui.Ui_CREATOR_GUI.setWindowTitle(create.project_location)
        except:
            ui.Ui_WARNING_GUI.show()
            ui.Ui_WARNING_UI.body.setText("An error occurred when choosing file location. Please choose again.")
        
    def new_project():
        create.project_location=False
        create.new_project=True
        ui.Ui_CREATOR_GUI.setWindowTitle("New*")
        ui.Ui_CREATOR_UI.list.clear()
    #saves the question dictionary in the qcq file    
    def save_file():
        if create.project_location:
            try:
                FILE=open(create.project_location, "wb")
                FILE.write(base64.b64encode(str(create.project_DATA).encode("ascii")))
                FILE.close()
            except:
                ui.Ui_WARNING_GUI.show()
                ui.Ui_WARNING_UI.body.setText("An error occurred while trying to save the file. Is the path still there?")
        else:
            if create.new_project:
                try:
                    create.project_location=QtWidgets.QFileDialog.getSaveFileName(ui.Ui_CREATOR_GUI, 'Save file', 'c:\\',"Quardcard Question File (*.qcq)")[0]
                    FILE=open(create.project_location, "wb")
                    FILE.write(base64.b64encode(str(create.project_DATA).encode("ascii")))
                    FILE.close()
                    ui.Ui_CREATOR_GUI.setWindowTitle(create.project_location)
                    create.new_project=False
                except:
                    ui.Ui_WARNING_GUI.show()
                    ui.Ui_WARNING_UI.body.setText("An error occurred when choosing the storage location. Please choose again.")
            else:
                ui.Ui_WARNING_GUI.show()
                ui.Ui_WARNING_UI.body.setText("You need to create a project before you can save it.")

class options_multiple_choice_question:
    Answers=[]
    def open_options():
        for count in range(16):
            eval("ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.answer_true_"+str(count+1)+".setChecked(0)")
            eval("ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.answer_text_"+str(count+1)+".setText('')")

        ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_GUI.show()
        ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.question.setText("")
    def save_question():
        elements=[]
        options_multiple_choice_question.Answers=[]
        for count in range(16):
            element_text=eval("ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.answer_text_"+str(count+1))
            element_checkbox=eval("ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.answer_true_"+str(count+1))
            if element_text.text()!='':
                options_multiple_choice_question.Answers.append([element_text.text(),element_checkbox.isChecked()])
               
        create.project_DATA.append({"NAME": ui.Ui_CREATOR_UI.name.text(),'TYPE': 'muliple_choice',"Question": ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.question.text() ,'Answers': options_multiple_choice_question.Answers})   
        print(create.project_DATA)
        
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("question_multiple_choice/question_multiple_choice.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        item.setText(ui.Ui_CREATOR_UI.name.text())
        ui.Ui_CREATOR_UI.list.addItem(item)
        
        ui.Ui_CREATOR_UI.name.setText("")        
        ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_GUI.close()
    
class options_question_entry:

    def open_options():
        ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_GUI.show()

    def save_question():
        create.project_DATA.append({"NAME": ui.Ui_CREATOR_UI.name.text(),'TYPE': 'entry', 'Question': ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.question.text(), 'Answer': ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.answer.text(), "TestULcase": ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.careonlettersize.checkState()})
        
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("question_entry/question_entry.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        item.setText(ui.Ui_CREATOR_UI.name.text())
        ui.Ui_CREATOR_UI.list.addItem(item)
         
        ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.question.setText("")
        ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.answer.setText("")
        ui.Ui_CREATOR_UI.name.setText("")
        ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_GUI.close()

class options_index_card:
    def open_options():
        ui.Ui_CREATOR_INDEX_CARD_OPTIONS_GUI.show()
        print("Hallo")
      
    def save_question():
        create.project_DATA.append({"NAME": ui.Ui_CREATOR_UI.name.text(),'TYPE': 'index_card', 'SIDE-A': ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI.frontside.text(), 'SIDE-B': ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI.backside.text()})
        
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("index_card/index_card.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        item.setText(ui.Ui_CREATOR_UI.name.text())
        ui.Ui_CREATOR_UI.list.addItem(item)
         
        ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI.frontside.setText("")
        ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI.backside.setText("")
        ui.Ui_CREATOR_UI.name.setText("")
        ui.Ui_CREATOR_INDEX_CARD_OPTIONS_GUI.close()
        
 
class options_radio_question:



     def open_options():
         ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_GUI.show()

     def save_question():

        checked=[]
        checked_right=[]
        right_answers=[]
        answers=[]


        name=ui.Ui_CREATOR_UI.name.text()

        question=ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.question.text()




        answers.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_text_1.text())
        answers.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_text_2.text())
        answers.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_text_3.text())
        answers.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_text_4.text())

        for count in range (len(answers)):
            if answers[count]=='':
                pass

            else:
                right_answers.append(answers[count])



        checked.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_true_1.isChecked())
        checked.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_true_2.isChecked())
        checked.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_true_3.isChecked())
        checked.append(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.answer_true_4.isChecked())


        for cnt in range (len(right_answers)):
            if checked[cnt]==True:
                checked_right.append(1)

            if checked[cnt]==False:
                checked_right.append(0)


        create.project_DATA.append({"NAME": name,'TYPE': 'radio_question','question': question,  'answers': right_answers,'right_answer': checked_right})
        print(create.project_DATA)
        
        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("question_radio/question_radio.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        item.setText(ui.Ui_CREATOR_UI.name.text())
        ui.Ui_CREATOR_UI.list.addItem(item)
        
        ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_GUI.close()

class options_order_question:
    add_number=0
    last_selected_index=0

    def open_options():
        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_GUI.show()

    def save_question():
        index=0
        items=[]
        question=""
        for cnt in range(options_order_question.add_number):
            try:
                items.append(ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.item(cnt).text())
            except:
                break

        question=ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.question.text()

        name=ui.Ui_CREATOR_UI.name.text()

        create.project_DATA.append({"NAME": name,'TYPE': 'order', 'Items': items, "Question": question, "Active": True})




        item = QtWidgets.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("question_order/question_order.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        item.setText(ui.Ui_CREATOR_UI.name.text())
        ui.Ui_CREATOR_UI.list.addItem(item)

        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_GUI.close()


    def change_text():
        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.item(options_order_question.last_selected_index).setText(ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.name.text())


    def add_item():

        name=ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.name.text()
        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.addItem(name)
        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.name.clear()

        options_order_question.add_number=options_order_question.add_number+1
        
    def last_selected():
        options_order_question.last_selected_index=ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.selectedIndexes()[0].row()
        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.name.setText(ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.item(options_order_question.last_selected_index).text())

    def remove_selected():
        ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.takeItem(options_order_question.last_selected_index)
        
        
class main:
    #define class Variables
    DATA_preload=[{"NAME": "Frage1", 'TYPE': 'entry', 'Question': 'Titel', 'Answer': 'true'},
          {"NAME": "Frage2","FAV":1,'TYPE': 'index_card', 'SIDE-A': 'text', 'SIDE-B': 'antwort'},
          {"NAME": "Frage3",'TYPE': 'order', 'Items': ["item1", "item2", "item3"], "Question": "Mach die richtige reihe", "Active": True},
          {"NAME": "Frage4",'TYPE': 'radio_question','question': 'Wie geht es dir',  'answers': ["answer1", "answer2", "answer3", ],'right_answer': [0, 0, 1, ] },
          {"NAME": "Frage5",'TYPE': 'muliple_choice',"Question": "Fragetittel" ,'Answers': [["Antwort1", False], ["Antwort2", True], ["Antwort3", False]]}]
    DATA=[]
    #DATA=[{'NAME': 'lol', 'TYPE': 'index_card', 'SIDE-A': 'Oben', 'SIDE-B': 'Unten'}]
    ENABLED=[]
    project_location="./"
    current_item_index=0
    Q_GAMETYPE="cash"
    for index in range(len(DATA)):
            ENABLED.append(True)
    Q_INDEX=0
    Q_NUMBER=0
    
    
    #btn previous or next pressed with index -1/1
    def btn_seek_pressed(index=0, customindex="NONE"):
        if customindex!="NONE":
            main.Q_INDEX=customindex
        else:
            main.Q_INDEX+=index
        
        if main.Q_INDEX<=0:
            ui.btn_previous.setEnabled(0)
            ui.btn_previous_fav.setEnabled(0)
        elif main.Q_INDEX>=len(main.DATA)-1:
            ui.btn_next.setEnabled(0)
            ui.btn_next_fav.setEnabled(0)
        elif main.Q_GAMETYPE!="time":
            ui.btn_next.setEnabled(1)
            ui.btn_next_fav.setEnabled(1)
            ui.btn_previous.setEnabled(1)
            ui.btn_previous_fav.setEnabled(1)
        
        #if index is out of question list, set index back
        if ((len(main.DATA)-1)<main.Q_INDEX) or main.Q_INDEX<0:
            main.Q_INDEX-=index
        
        #check witch question type and start equal class
        else:
            ui.list_questions.setCurrentRow(main.Q_INDEX)
            if main.DATA[main.Q_INDEX]["TYPE"]=="index_card":
                ui.bg.raise_()
                ui.index_card_obj.raise_()
                index_card.side=0
                index_card.prg(main.DATA[main.Q_INDEX], main.Q_INDEX)
                
            elif main.DATA[main.Q_INDEX]["TYPE"]=="radio_question":
                ui.bg.raise_()
                ui.question_radio.raise_()
                radio_question.prg(main.DATA[main.Q_INDEX], main.Q_INDEX)
                
            elif main.DATA[main.Q_INDEX]["TYPE"]=="muliple_choice":
                ui.bg.raise_()
                ui.question_muliple_choice.raise_()
                multiple_choice.prg(main.DATA[main.Q_INDEX], main.Q_INDEX)
            
            elif main.DATA[main.Q_INDEX]["TYPE"]=="entry":
                ui.bg.raise_()
                ui.question_entry.raise_()
                entry.prg(main.DATA[main.Q_INDEX], main.Q_INDEX)
                
            elif main.DATA[main.Q_INDEX]["TYPE"]=="order":
                ui.bg.raise_()
                ui.question_order.raise_()
                ui.question_order_list.clear()
                order.prg(main.DATA[main.Q_INDEX], main.Q_INDEX)
                
            #if question type not implemented, show unsupported question
            else:
                ui.bg.raise_()
                ui.unsupported_question.raise_()
                ui.unsupported_question_label.setText("Unsupported Question '"+main.DATA[main.Q_INDEX]["TYPE"]+"'")
               
        #try to set progressbar value
        try:
            ui.progressbar_progress.setValue(main.Q_INDEX+1)
            ui.btn_fav.setChecked(main.DATA[main.Q_INDEX]["FAV"])
        except:
            ui.btn_fav.setChecked(0)
        
    #open about window
    def open_about():
        ui.Ui_ABOUT_GUI.show()
        
    #open chose file window
    def event_handler(parameter={}):
        if main.Q_GAMETYPE=="cash":
            main.cash_add_remove(count=parameter["POINTS"])
        elif main.Q_GAMETYPE=="time":
            main.time_add_remove(count=parameter["TIME"])
        
    def choose_file():
        ui.list_questions.clear()
        ui.lcd_score.setText("0")
        main.Q_GAMETYPE=""
        ui.btn_previous_fav.setEnabled(0)
        ui.btn_previous.setEnabled(0)
        ui.btn_next_fav.setEnabled(0)
        ui.btn_next.setEnabled(0)
        ui.btn_fav.setEnabled(0)
        ui.btn_show_answers.setEnabled(0)
        ui.btn_liveedit.setEnabled(0)
        ui.list_questions.setEnabled(0)
        ui.progressbar_progress.setMaximum(0)
        try:
            main.DATA=[]
            main.project_location=QtWidgets.QFileDialog.getOpenFileName(gui, 'Open file', 'c:\\',"Quardcard Question File (*.qcq)")[0]
            FILE=open(main.project_location,"rb")
            main.DATA_preload=eval(base64.b64decode(FILE.read().decode("ascii")))
            FILE.close()
            ui.progressbar_progress.setValue(0)
            ui.bg.raise_()
            ui.preload.raise_()
            
            main.start_break()
        except:
            main.start_break()
            main.DATA_preload=[]
            main.Q_NUMBER=0
            ui.bg.raise_()
            ui.unsupported_question.raise_()
            ui.unsupported_question_label.setText("Unsupported or broken path")
        
    #start opend question file
    def start_private_normal():
        main.Q_INDEX=0
        main.Q_GAMETYPE="cash"
        main.DATA=main.DATA_preload
        main.Q_NUMBER=len(main.DATA)
        ui.progressbar_progress.setMaximum(main.Q_NUMBER)
        main.ENABLED=[]
        for index in range(main.Q_NUMBER):
            main.ENABLED.append(True)
        ui.time_mode.setHidden(1)
        ui.cash_mode.setHidden(0)
        ui.btn_previous_fav.setEnabled(1)
        ui.btn_previous.setEnabled(1)
        ui.btn_next_fav.setEnabled(1)
        ui.btn_next.setEnabled(1)
        ui.btn_fav.setEnabled(1)
        ui.btn_show_answers.setEnabled(1)
        ui.btn_liveedit.setEnabled(1)
        ui.list_questions.setEnabled(1)
        ui.list_questions.clear()
        playsound.playsound("sounds/START_CASH.wav", False)
        for element in main.DATA:
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            try:
                if element["FAV"]==True:
                    icon.addPixmap(QtGui.QPixmap("general/favourite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            except:
                pass
            item.setIcon(icon)
            item.setText(element["NAME"])
            ui.list_questions.addItem(item)
        main.btn_seek_pressed(index=0)
        
    def start_private_time():
        main.Q_INDEX=0
        main.Q_GAMETYPE="time"
        main.DATA=main.DATA_preload
        main.Q_NUMBER=len(main.DATA)
        ui.progressbar_progress.setMaximum(main.Q_NUMBER)
        main.ENABLED=[]
        for index in range(main.Q_NUMBER):
            main.ENABLED.append(True)
        ui.time_mode.setHidden(0)
        ui.cash_mode.setHidden(1)
        ui.btn_previous_fav.setEnabled(0)
        ui.btn_previous.setEnabled(0)
        ui.btn_next_fav.setEnabled(0)
        ui.btn_next.setEnabled(0)
        ui.btn_fav.setEnabled(0)
        ui.btn_show_answers.setEnabled(0)
        ui.btn_liveedit.setEnabled(0)
        ui.list_questions.setEnabled(0)
        ui.list_questions.clear()
        for element in main.DATA:
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            try:
                if element["FAV"]==True:
                    icon.addPixmap(QtGui.QPixmap("general/favourite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            except:
                pass
            item.setIcon(icon)
            item.setText(element["NAME"])
            ui.list_questions.addItem(item)
        playsound.playsound("sounds/START_CLOCK.wav", False)
        main.btn_seek_pressed(index=0)
        ui.lcd_time.setText(str(65))
        main.time_timer()

    def time_timer():
        while main.Q_GAMETYPE=="time" and ui.lcd_time.text()!="0":
            a=ui.lcd_time.text()
            ui.lcd_time.setText(str(int(a)-1))
            if int(a)-1 <= 15:
                playsound.playsound("sounds/POINTS_DOWN.wav", 0)
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1000, loop.quit)
            loop.exec_()
        
        playsound.playsound("sounds/SPECIAL.wav", 0)
        loop = QtCore.QEventLoop()
        QtCore.QTimer.singleShot(2000, loop.quit)
        loop.exec_()
        main.start_break()
        
    def time_add_remove(count):
        if count<0:
            playsound.playsound("sounds/ANSWER_FALSE_CLOCK.wav", False)
            for i in range(-count):
                playsound.playsound("sounds/POINTS_DOWN.wav", 0)
                a=ui.lcd_time.text()
                ui.lcd_time.setText(str(int(a)-1))
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(10, loop.quit)
                loop.exec_()
        elif count>0:
            playsound.playsound("sounds/ANSWER_TRUE_CLOCK.wav", False)
            for i in range(count):
                playsound.playsound("sounds/POINTS_UP.wav", 0)
                a=ui.lcd_time.text()
                ui.lcd_time.setText(str(int(a)+1))
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(10, loop.quit)
                loop.exec_()
            
            if main.Q_INDEX==len(main.DATA)-1:
                playsound.playsound("sounds/SPECIAL.wav", 0)
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(2000, loop.quit)
                loop.exec_()
                main.start_break()
            else:
                main.btn_seek_pressed(index=1)
        
    def cash_add_remove(count=0):
        if count<0:
            playsound.playsound("sounds/ANSWER_FALSE.wav", False)
            for i in range(-count):
                playsound.playsound("sounds/POINTS_DOWN.wav", 0)
                a=ui.lcd_score.text()
                ui.lcd_score.setText(str(int(a)-1))
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(10, loop.quit)
                loop.exec_()
        elif count>0:
            playsound.playsound("sounds/ANSWER_TRUE.wav", False)
            for i in range(count):
                playsound.playsound("sounds/POINTS_UP.wav", 0)
                a=ui.lcd_score.text()
                ui.lcd_score.setText(str(int(a)+1))
                loop = QtCore.QEventLoop()
                QtCore.QTimer.singleShot(10, loop.quit)
                loop.exec_()
        
    def btn_fav_pressed():
        try:
            if main.DATA[main.current_item_index]["FAV"]:
                main.DATA[main.current_item_index]["FAV"]=False
            else:
                main.DATA[main.current_item_index]["FAV"]=True
        except:
            try:
                main.DATA[main.current_item_index]["FAV"]=True
            except:
                pass
            
        FILE=open(main.project_location, "wb")
        FILE.write(base64.b64encode(str(main.DATA).encode("ascii")))
        FILE.close()
        print(ui.list_questions.selectedIndexes())
        ui.list_questions.clear()
        for element in main.DATA:
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            try:
                if element["FAV"]==True:
                    icon.addPixmap(QtGui.QPixmap("general/favourite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            except:
                pass
            item.setIcon(icon)
            item.setText(element["NAME"])
            ui.list_questions.addItem(item)
    
    def live_edit_save():
        main.DATA[main.current_item_index]=eval(ui.Ui_LIVE_EDIT_UI.text.text())
        FILE=open(main.project_location, "wb")
        FILE.write(base64.b64encode(str(main.DATA).encode("ascii")))
        FILE.close()
        ui.list_questions.clear()
        for element in main.DATA:
            item = QtWidgets.QListWidgetItem()
            icon = QtGui.QIcon()
            try:
                if element["FAV"]==True:
                    icon.addPixmap(QtGui.QPixmap("general/favourite.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            except:
                pass
            item.setIcon(icon)
            item.setText(element["NAME"])
            ui.list_questions.addItem(item)
        main.btn_seek_pressed(index=0)
        ui.Ui_LIVE_EDIT_GUI.close()
        
    def live_edit_open():
        ui.Ui_LIVE_EDIT_UI.text.setText(str(main.DATA[main.current_item_index]))
        ui.Ui_LIVE_EDIT_GUI.show()
    
    def list_item_selected():
        main.current_item_index=ui.list_questions.currentIndex().row()
        main.btn_seek_pressed(customindex=main.current_item_index)
        
    def start_break():
        main.Q_INDEX=0
        main.Q_GAMETYPE=""
        main.DATA=[]
        ui.progressbar_progress.setValue(0)
        ui.time_mode.setHidden(1)
        ui.cash_mode.setHidden(1)
        ui.btn_previous_fav.setEnabled(0)
        ui.btn_previous.setEnabled(0)
        ui.btn_next_fav.setEnabled(0)
        ui.btn_next.setEnabled(0)
        ui.btn_fav.setEnabled(0)
        ui.btn_show_answers.setEnabled(0)
        ui.btn_liveedit.setEnabled(0)
        ui.list_questions.setEnabled(0)
        ui.progressbar_progress.setMaximum(0)
        ui.list_questions.clear()
        ui.bg.raise_()
        ui.preload.raise_()
        ui.lcd_score.setText("0")
        playsound.playsound("sounds/START.wav", False)
        
    #start creator window
    def start_creator():
        ui.Ui_CREATOR_GUI.show()
    
    def show_answers():
        try:    
            if main.DATA[main.Q_INDEX]["TYPE"]=="index_card":
                index_card.prg(main.DATA[main.Q_INDEX], main.Q_INDEX)
            
            else:
                main.ENABLED[main.Q_INDEX]=False
                main.event_handler(parameter={"POINTS": -20})
                main.btn_seek_pressed(index=0)
        except:
            pass
        
class boot:
    def LICENCE_AGREED():
        LICENCE_AGREED=ui.Ui_SETUP_UI.LICENSE_TERMS_ACCEPT_CHECKBOX.checkState()
        if not LICENCE_AGREED:
            gui.close()
            ui.Ui_SETUP_GUI.close()
            
    def LICENCE_CLOSED():
        LICENCE_AGREED=ui.Ui_SETUP_UI.LICENSE_TERMS_ACCEPT_CHECKBOX.checkState()
        if not LICENCE_AGREED:
            gui.close()
            ui.Ui_SETUP_GUI.close()
        else:
            ui.Ui_SETUP_GUI.close()
            gui.show() 
            
class SETTINGS:
    def save():
        FILE=open("SETTINGS.txt", "w")
        FILE.write(ui.Ui_SETTINGS_UI.stylesheet.currentText()+"\n"+ui.Ui_SETTINGS_UI.style.currentText()+"\n"+ui.Ui_SETTINGS_UI.colormode.currentText()+"\n"+ui.Ui_SETTINGS_UI.maxsizemode.currentText())
        FILE.close()
        ui.Ui_SETTINGS_GUI.close()
        
        
#create a window for the application
app=QtWidgets.QApplication(sys.argv)
app.setStyle(SETTINGS_STYLE[:-1])
gui=QtWidgets.QMainWindow()
ui=Ui_MAINWINDOW()
ui.setupUi(gui)

ui.Ui_SETUP_GUI=QtWidgets.QWizard()
ui.Ui_SETUP_UI=Ui_LICENSE_WIZARD()
ui.Ui_SETUP_UI.setupUi(ui.Ui_SETUP_GUI)
        
ui.Ui_SETUP_GUI.show()

ui.Ui_SETUP_GUI.button(QtWidgets.QWizard.NextButton).clicked.connect(lambda: boot.LICENCE_AGREED())
ui.Ui_SETUP_GUI.button(QtWidgets.QWizard.FinishButton).clicked.connect(lambda: boot.LICENCE_CLOSED())

ui.Ui_ABOUT_GUI=QtWidgets.QDialog()
ui.Ui_ABOUT_UI=Ui_ABOUT()
ui.Ui_ABOUT_UI.setupUi(ui.Ui_ABOUT_GUI)
ui.Ui_ABOUT_UI.ok.clicked.connect(lambda: ui.Ui_ABOUT_GUI.close())

ui.Ui_CREATOR_GUI=QtWidgets.QMainWindow()
ui.Ui_CREATOR_UI=Ui_CREATE()
ui.Ui_CREATOR_UI.setupUi(ui.Ui_CREATOR_GUI)

ui.Ui_CREATOR_INDEX_CARD_OPTIONS_GUI=QtWidgets.QDialog()
ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI=Ui_OPTIONS_INDEX_CARD()
ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI.setupUi(ui.Ui_CREATOR_INDEX_CARD_OPTIONS_GUI)


#makes the option window for the question entry
ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_GUI=QtWidgets.QDialog()
ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI=Ui_OPTIONS_QUESTION_ENTRY()
ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.setupUi(ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_GUI)


ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_GUI=QtWidgets.QDialog()
ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI=Ui_OPTIONS_MULTIPLE_CHOICE()
ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.setupUi(ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_GUI)


ui.Ui_WARNING_GUI=QtWidgets.QDialog()
ui.Ui_WARNING_UI=Ui_WARNING()
ui.Ui_WARNING_UI.setupUi(ui.Ui_WARNING_GUI)
ui.Ui_WARNING_UI.cont.clicked.connect(lambda: ui.Ui_WARNING_GUI.close())

ui.Ui_SETTINGS_GUI=QtWidgets.QDialog()
ui.Ui_SETTINGS_UI=Ui_SETTINGS()
ui.Ui_SETTINGS_UI.setupUi(ui.Ui_SETTINGS_GUI)
ui.Ui_SETTINGS_UI.save.clicked.connect(lambda: SETTINGS.save())

ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_GUI=QtWidgets.QDialog()
ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI=Ui_OPTIONS_QUESTION_RADIO()
ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.setupUi(ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_GUI)

ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_GUI=QtWidgets.QDialog()
ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI=Ui_OPTIONS_QUESTION_ORDER()
ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.setupUi(ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_GUI)
ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.itemClicked.connect(lambda: options_order_question.last_selected())
ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.remove.clicked.connect(lambda: options_order_question.remove_item())
ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.add.clicked.connect(lambda: options_order_question.add_item())

ui.Ui_LIVE_EDIT_GUI=QtWidgets.QDialog()
ui.Ui_LIVE_EDIT_UI=Ui_LIVE_EDIT()
ui.Ui_LIVE_EDIT_UI.setupUi(ui.Ui_LIVE_EDIT_GUI)
ui.Ui_LIVE_EDIT_UI.save.clicked.connect(lambda: main.live_edit_save())

ui.Ui_CREATOR_QUESTION_RADIO_OPTIONS_UI.save.clicked.connect(lambda: options_radio_question.save_question())
 
#buttons for the class main       
ui.btn_next.clicked.connect(lambda: main.btn_seek_pressed(index=1))
ui.btn_previous.clicked.connect(lambda: main.btn_seek_pressed(index=-1))


ui.btn_fav.clicked.connect(lambda: main.btn_fav_pressed())
#button to turn the index cards       
ui.index_card_obj_btn.clicked.connect(lambda: index_card.prg(index_card.data, main.Q_INDEX))

#buttons for the order class and the function to the button
ui.question_order_list.itemClicked.connect(lambda: order.last_selected())
ui.question_order_test.clicked.connect(lambda: order.test())
ui.btn_down.clicked.connect(lambda: order.down())
ui.btn_up.clicked.connect(lambda: order.up())

#button for the radio_question class
ui.question_radio_checkbox_test.clicked.connect(lambda: radio_question.test())

#button for the question_entry class
ui.question_entry_test.clicked.connect(lambda: entry.test())

ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.remove.clicked.connect(lambda: options_order_question.last_selected())

#button for the multiple_choice class
ui.question_muliple_choice_test.clicked.connect(lambda: multiple_choice.test())

ui.list_questions.currentRowChanged.connect(lambda: main.list_item_selected())

ui.actionTime.triggered.connect(lambda: main.start_private_time())

ui.actionBreak.triggered.connect(lambda: main.start_break())
#open the about window
ui.actionAbout.triggered.connect(lambda: main.open_about())
#open the choose file window
ui.actionOpen.triggered.connect(lambda: main.choose_file())
#start the programm with your questions
ui.actionNormal.triggered.connect(lambda: main.start_private_normal())
#start the creater
ui.actionCreate.triggered.connect(lambda: main.start_creator())

#add element button
ui.Ui_CREATOR_UI.btn_add.clicked.connect(lambda: create.btn_add())

#open file btn
ui.Ui_CREATOR_UI.actionOpenproject.triggered.connect(lambda: create.open_file())

ui.btn_liveedit.clicked.connect(lambda: main.live_edit_open())
#
ui.Ui_CREATOR_UI.actionAbout.triggered.connect(lambda: main.open_about())

ui.Ui_CREATOR_UI.actionNewproject.triggered.connect(lambda: create.new_project())

ui.Ui_CREATOR_UI.actionSaveproject.triggered.connect(lambda: create.save_file())

ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.remove.clicked.connect(lambda: ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.list.takeItem(options_order_question.last_selected_index))

#close the window
ui.actionExit.triggered.connect(lambda: gui.close())
ui.actionSettings.triggered.connect(lambda: ui.Ui_SETTINGS_GUI.show())


ui.Ui_CREATOR_INDEX_CARD_OPTIONS_UI.save.clicked.connect(lambda: options_index_card.save_question())

#save options from the question entry option window
ui.Ui_CREATOR_QUESTION_ENTRY_OPTIONS_UI.save.clicked.connect(lambda: options_question_entry.save_question())

ui.Ui_CREATOR_QUESTION_MULTIPLE_CHOICE_OPTIONS_UI.save.clicked.connect(lambda: options_multiple_choice_question.save_question())

ui.Ui_CREATOR_QUESTION_ORDER_OPTIONS_UI.save.clicked.connect(lambda: options_order_question.save_question())

#base64.b64encode(str(main.DATA).encode("ascii"))

ui.btn_show_answers.clicked.connect(lambda: main.show_answers())

#ui.Ui_ABOUT_UI.ok.clicked.connect(lambda: ui.Ui_ABOUT_GUI.close())

#that it starts with index 0 and not 1
ui.time_mode.setHidden(1)
ui.cash_mode.setHidden(1)

if "blackwhite" in SETTINGS_COLORMODE:
    ui.bg_wide.setEnabled(0)
    
if "disable" in SETTINGS_MAXSIZE:
    gui.setMaximumSize(10000,10000)

app.exec_()