import pandas as pd
import matplotlib.pyplot as plt
def plotting(x1):
    a1=x1.Date
    b1=x1.Close
    c1=x1.tail(10)
    d1=c1.Date
    e1=c1.Close

    plt.figure(figsize=(10,5))
    
    plt.subplot(2,1,1)
    plt.plot(a1,b1)
    plt.xticks(rotation=0)
    plt.title("WEEKLY DATA")
    plt.xlabel("Date")
    plt.subplots_adjust(hspace=0.5)
    plt.ylabel("Value of stock")

    plt.subplot(2,1,2)
    plt.plot(d1,e1)
    plt.xticks(rotation=45)
    plt.title("DATA ON MONTHLY BASIS ")
    plt.xlabel("Date")
    plt.subplots_adjust(hspace=0.5)
    plt.ylabel("Value of stock")
    plt.show()

def files():
    x1=pd.read_csv("output.csv")
    plotting(x1)
