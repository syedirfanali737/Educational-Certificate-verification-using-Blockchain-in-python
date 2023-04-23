from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from Block import *
from Blockchain import *
from hashlib import sha256
import re
import os
mobile_number_regex = re.compile(r'^[6789]\d{9}$')
main = Tk()
main.title(" BVRIT Educational Certificate Validation")
main.geometry("1000x1100")

global filename

blockchain = Blockchain()
if os.path.exists('blockchain_contract.txt'):
    with open('blockchain_contract.txt', 'rb') as fileinput:
        blockchain = pickle.load(fileinput)
    fileinput.close()

def is_valid_mobile_number(mobile_number):
    return bool(mobile_number_regex.match(mobile_number))
def saveCertificate():
    global filename
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "certificate_templates")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    roll_no = tf1.get()
    name = tf2.get()
    contact = tf3.get()
    batch_no = tf4.get()
    passout_year_month = tf5.get()
    auth_certi = tf6.get()
    
    
    if len(roll_no) > 0 and len(name) > 0 and len(contact) > 0 and len(batch_no) > 0 and len(passout_year_month) > 0 and len(auth_certi) and is_valid_mobile_number(contact):
        digital_signature = sha256(bytes).hexdigest();
        data = roll_no+"#"+name+"#"+contact+"#"+digital_signature+"#"+batch_no+"#"+passout_year_month+"#"+auth_certi
        blockchain.add_new_transaction(data)
        hash = blockchain.mine()
        b = blockchain.chain[len(blockchain.chain)-1]
        text.insert(END,"Blockchain Previous Hash : "+str(b.previous_hash)+"\nBlock No : "+str(b.index)+"\nCurrent Hash : "+str(b.hash)+"\n")
        text.insert(END,"Certificate Digital Signature : "+str(digital_signature)+"\n\n")
        blockchain.save_object(blockchain,'blockchain_contract.txt')
    else:
        text.insert(END,"Please Check the Data and Enter Correctly")

def verifyCertificate():
    text.delete('1.0', END)
    filename = askopenfilename(initialdir = "certificate_templates")
    with open(filename,"rb") as f:
        bytes = f.read()
    f.close()
    digital_signature = sha256(bytes).hexdigest();
    flag = True
    for i in range(len(blockchain.chain)):
        if i > 0:
            b = blockchain.chain[i]
            data = b.transactions[0]
            arr = data.split("#")
            if arr[3] == digital_signature:
                text.insert(END,"Certificate Uploaded\n")
                text.insert(END,"Details extracted from Blockchain after Validation\n\n")
                text.insert(END,"Digital Sign : "+arr[3]+"\n")
                text.insert(END,"Roll No : "+arr[0]+"\n")
                text.insert(END,"Student Name : "+arr[1]+"\n")
                text.insert(END,"Contact No   : "+arr[2]+"\n")
                text.insert(END,"Batch No     : "+arr[4]+"\n")
                text.insert(END,"Passed Out Year and Month    : "+arr[5]+"\n")
                text.insert(END,"Certificate Authorized By    : "+arr[6]+"\n")


                flag = False
                break
    if flag:
        text.insert(END,"Verification Failed or  Certificate Forged")
    

font = ('times', 18, 'bold')
title = Label(main, text='B V Raju Institute of Technology\n Educational Certificate Validation')
title.config(bg='bisque', fg='purple1')  
title.config(font=font)           
title.config(height=3, width=75)       
title.place(x=0,y=5)

font1 = ('times', 13, 'bold')

l1 = Label(main, text='Roll No :')
l1.config(font=font1)
l1.place(x=50,y=100)

tf1 = Entry(main,width=20)
tf1.config(font=font1)
tf1.place(x=180,y=100)

l2 = Label(main, text='Student Name :')
l2.config(font=font1)
l2.place(x=50,y=150)

tf2 = Entry(main,width=20)
tf2.config(font=font1)
tf2.place(x=180,y=150)

l3 = Label(main, text='Contact No :')
l3.config(font=font1)
l3.place(x=50,y=200)

tf3 = Entry(main,width=20)
tf3.config(font=font1)
tf3.place(x=180,y=200)

l4 = Label(main, text='Batch No :')
l4.config(font=font1)
l4.place(x=500,y=100)

tf4 = Entry(main,width=20)
tf4.config(font=font1)
tf4.place(x=730,y=100)

l5 = Label(main, text='Passout Year and Month :')
l5.config(font=font1)
l5.place(x=500,y=150)

tf5 = Entry(main,width=20)
tf5.config(font=font1)
tf5.place(x=730,y=150)

l6 = Label(main, text='Certificate Authorized by :')
l6.config(font=font1)
l6.place(x=500,y=200)

tf6 = Entry(main,width=20)
tf6.config(font=font1)
tf6.place(x=730,y=200)

saveButton = Button(main, text="Save Certificate with Digital Signature", command=saveCertificate)
saveButton.place(x=50,y=300)
saveButton.config(font=font1)

verifyButton = Button(main, text="Verify Certificate", command=verifyCertificate)
verifyButton.place(x=420,y=300)
verifyButton.config(font=font1)

font1 = ('times', 13, 'bold')
text=Text(main,height=15,width=120)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=400)
text.config(font=font1)
main.config(bg='white')
main.mainloop()


