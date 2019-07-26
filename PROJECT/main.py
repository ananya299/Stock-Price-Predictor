import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tkinter
from tkinter import scrolledtext
from tkinter import *
import pandas as pd
from yahoo_fin import stock_info as si
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor
from tkinter import messagebox
from nsetools import Nse

nse = Nse()
window = tkinter.Tk()
window.configure(background='black')
#window.overrideredirect(1)
company_name = StringVar()
pred_val1 = StringVar()
pred_val2 = StringVar()
companyname = ""
data=''
a = ["TECHNOLOGY","HEALTHCARE","FINANCIAL","AUTO","ENERGY"]
selectcat = StringVar(window)
selectcat.set(a[0])

def get_company_name():
    window.lift()
    try:
        print("company name")
        company_name.set("TICKER: "+company_name_text.get().upper())
        companyname=str(company_name_text.get().upper())
        quotes_df = si.get_data(str(companyname))
        global data
        data = quotes_df.copy()
        linreg = LinearRegression()
        gb = GradientBoostingRegressor(n_estimators=200)

        pred_val1.set("Predicted Closing Price: "+str(make_prediction(quotes_df, linreg, 0)))
        pred_val2.set("Predicted Closing Price: "+str(make_prediction(quotes_df, gb, 1)))

        #print('Predicted Closing Price by linear reg: %.2f\n' % make_prediction(quotes_df, linreg, 0))
        #print('Predicted Closing Price: %.2f\n' % make_prediction(quotes_df, gb, 1))


    except:
        messagebox.showinfo('ERROR','Invalid company name.Please try again.')


def show_graphs(flag,df2):
    window.lift()
    print("show_graphs")
    cname = tkinter.Label(window, textvariable=company_name, font=("Arial", 30))
    cname.grid(column=1, row=0, padx=5,rowspan=1)

    cpred=tkinter.Label(window,textvariable=pred_val2,font=("Arial",30))
    cpred.grid(column=2,row=0,padx=5,rowspan=1)

    #GRAPH 1
    figure1 = plt.figure(figsize=(8,4))
    chart_type1 = FigureCanvasTkAgg(figure1, window)
    chart_type1.get_tk_widget().grid(column=1,padx=15,row=1,rowspan=7)
    plt.plot(df2['open'].tail(150), label='OPEN PRICE')
    plt.plot(df2['high'].tail(150), label='HIGH PRICE')
    plt.plot(df2['low'].tail(150),  label='LOW PRICE')
    plt.plot(df2['close'].tail(150),label='CLOSE PRICE')
    plt.legend()
    plt.title('ORIGINAL VALUES')

    #TABLE
    table1 = tkinter.scrolledtext.ScrolledText(window, width=97, height=25)
    table1.grid(column=2,padx=10,row=1,rowspan=7)
    features_to_fit = ['open', 'high', 'low', 'close', 'volume']
    table1.insert(tkinter.INSERT,df2[features_to_fit])


    #GRAPH 2
    if(flag==0):
        figure2 = plt.figure(figsize=(8,4))
        chart_type2 = FigureCanvasTkAgg(figure2, window)
        chart_type2.get_tk_widget().grid(column=2,padx=15,row=8)
        plt.plot(df2['close'].tail(200), color='blue',label='ORIGINAL')
        plt.plot(df2['NextClose'].tail(200), color='orange',label='PRIDICTED')
        plt.xlabel("DATE")
        plt.ylabel("PRICE")
        plt.legend()
        plt.title('Orignal VS Predicited(LINEAR REGRESSION)')

    #GRAPH 3
    if(flag==1):
        figure3 = plt.figure(figsize=(8, 4))
        chart_type3 = FigureCanvasTkAgg(figure3, window)
        chart_type3.get_tk_widget().grid(column=1, padx=15, row=8)
        plt.plot(df2['close'].tail(200), color='blue', label='ORIGINAL')
        plt.plot(df2['NextClose'].tail(200), color='orange', label='PRIDICTED')
        plt.xlabel("DATE")
        plt.ylabel("PRICE")
        plt.legend()
        plt.title('Orignal VS Predicited(GradientBoostingRegressor)')

def show_Cat(a):
    print("Show_cat")
    window5 = tkinter.Tk()
    window5.geometry("1700x1080+165+0")
    window5.overrideredirect(1)
    table1 = tkinter.scrolledtext.ScrolledText(window5, width=200, height=50)
    table1.grid(column=2, padx=20, pady=20, row=1, rowspan=5)
    if(a=="TECHNOLOGY"):
        a1=pd.read_csv("technology.csv")
    if (a == "HEALTHCARE"):
        a1 = pd.read_csv("health.csv")
    if (a == "FINANCIAL"):
        a1 = pd.read_csv("finance.csv")
    if (a == "AUTO"):
        a1 = pd.read_csv("auto.csv")
    if (a == "ENERGY"):
        a1 = pd.read_csv("energy.csv")
    pd.set_option('display.max_columns', 30)
    table1.insert(tkinter.INSERT,a1[['Symbol','Name','Last price','Market time','Change','Market cap']])
    window5.mainloop()

def top5():
    print("top 5")
    window3 = tkinter.Tk()
    window3.geometry("1700x1080+165+0")
    window3.overrideredirect(1)
    gainers = nse.get_top_gainers()
    loser = nse.get_top_losers()
    cname = tkinter.Label(window3,text='TOP 5 GAINERS OF THE DAY', font=("Arial", 15))
    cname.grid(column=1, row=0, padx=5, rowspan=1)
    cname2 = tkinter.Label(window3, text='TOP 5 LOSERS OF THE DAY', font=("Arial", 15))
    cname2.grid(column=1, row=2, padx=5, rowspan=1)
    table1 = tkinter.scrolledtext.ScrolledText(window3, width=200, height=20)
    table2 = tkinter.scrolledtext.ScrolledText(window3, width=200, height=20)
    table1.grid(column=1, padx=30, pady=20, row=1, rowspan=1)
    table2.grid(column=1, padx=30, pady=20, row=3, rowspan=1)
    #pd.set_option('display.max_columns', 30)
    gain = pd.DataFrame.from_dict(gainers[0:5])
    lose = pd.DataFrame.from_dict(loser[0:5])
    table1.insert(tkinter.INSERT, gain[['symbol','highPrice','lowPrice', 'openPrice', 'previousPrice', 'turnoverInLakhs']])
    table2.insert(tkinter.INSERT,lose[['symbol', 'highPrice', 'lowPrice', 'openPrice', 'previousPrice', 'turnoverInLakhs']])
    window3.mainloop()



def show_log():
    print("show log")
    window2=tkinter.Tk()
    window2.geometry("1700x1080+165+0")
    window2.overrideredirect(1)
    table1 = tkinter.scrolledtext.ScrolledText(window2, width=200, height=50)
    table1.grid(column=2, padx=20, pady=20, row=1, rowspan=5)
    features_to_fit = ['open', 'high', 'low', 'close', 'volume']
    table1.insert(tkinter.INSERT, data[features_to_fit])
    window2.mainloop()


def show_list():
    print("show list")
    window4 = tkinter.Tk()
    window4.geometry("1700x1080+165+0")
    window4.overrideredirect(1)
    all_stock_codes = nse.get_stock_codes()
    table1 = tkinter.scrolledtext.ScrolledText(window4, width=200, height=50)
    table1.grid(column=2, padx=20, pady=20, row=1, rowspan=5)
    code=pd.DataFrame.from_dict(all_stock_codes,orient='index')
    table1.insert(tkinter.INSERT,code)
    window4.mainloop()


def make_prediction(quotes_df, estimator,flag):
    df = quotes_df.copy()
    df['ClosingPctChange'] = df['close'].pct_change()
    df_today = df.iloc[-1:, :].copy()
    df['NextClose'] = df['close'].shift(-1)
    df.dropna(inplace=True)
    features_to_fit = ['open', 'high', 'low', 'close', 'volume']
    X = df[features_to_fit]
    y = df['adjclose']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2)
    cv = cross_val_score(estimator, X_test, y_test)
    print('Accuracy:', cv.mean())
    estimator.fit(X, y)
    X_new = df_today[features_to_fit]
    next_price_prediction = estimator.predict(X_new)
    show_graphs(flag,df)
    return next_price_prediction



window.title("STOCK MARKET PREDICTION")
#window.geometry("1920x1080+0+0")
window.attributes('-fullscreen', True)

company_name_button = tkinter.Button(window, text="SEARCH COMPANY",width=20,height=5,command=get_company_name)
company_name_button.grid(column=0,pady=5,padx=5,row=0)

company_name_text = tkinter.Entry(window,width=20)
company_name_text.grid(column=0,pady=5,padx=5,row=1)

top5_button = tkinter.Button(window,text="TOP 5 COMPANIES",width=20,height=5,command=top5)
top5_button.grid(column=0,pady=5,padx=5,row=2)

show_log_button = tkinter.Button(window,text="SHOW LOG",width=20,height=5,command=show_log)
show_log_button.grid(column=0,pady=5,padx=5,row=3)

show_companies_list = tkinter.Button(window,text="SHOW LIST OF COMPANIES",width=20,height=5,command=show_list)
show_companies_list.grid(column=0,pady=5,padx=5,row=4)

type_companies_dropdown = OptionMenu(window,selectcat,*a,command=show_Cat)
type_companies_dropdown.grid(column=0,pady=5,padx=5,row=5)

exit_button = tkinter.Button(window,text="EXIT",width=20,height=5,command=exit)
exit_button.grid(column=0,pady=5,padx=5,row=7)

window.mainloop()