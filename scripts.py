import schedule
import time
from bs4 import BeautifulSoup
import requests
import smtplib
from flask import *
from email.message import EmailMessage

app = Flask(__name__)

s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
#s.starttls()
s.login("karsayan599@gmail.com", "*****************")	

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/last')
def last():
    return render_template('thanks.html')

@app.route('/evaluate',methods = ['GET','POST'])
def evaluate():
    if( request.method == 'POST'):
        URL = request.form['mywish']

        job = schedule.every(5).seconds.do(evaluate)
            
        r = requests.get(URL).text
        soup = BeautifulSoup(r,'html5lib')
            
        find_name = soup.find('span', class_ = 'B_NuCI') #this gives only the first search
        find_price = soup.find('div', class_ = '_30jeq3 _16Jk6d').text
        find_price_value = find_price.replace(",","")
        find_price_value2 = find_price_value.replace("₹","")
                    
        a = request.form['value'];
        email = request.form['credential']
		
		
		

		

        if (int(find_price_value2) < int(a)):
            msg = EmailMessage()
            msg.set_content("!!!!!ALERT!!!!\nPrice Dropped to {}\n\n{}\n\n\nUrl : {}".format(str(find_price_value2),find_name.text,URL))
            msg['Subject'] = 'Price Alert'
            msg['From'] = "karsayan599@gmail.com"
            msg['To'] = email
            s.send_message(msg)
            print('send')
            schedule.cancel_job(job)
            #quit()

        while True:
            if (int(find_price_value2) < int(a)):
                print("redirect")
                return redirect(url_for("last"))
                break
            else:
                schedule.run_pending()
                time.sleep(1)

    #s.quit()

if __name__ == '__main__':  
   app.run(debug = True) 

   



# mes = "hi, this is the mail sent by using the flask web application.: " + find_name.text + " : " + find_price_value2
    








    
    
