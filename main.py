import yfinance as yf
import pandas as pd
import Account
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

def plot(tickers):
    style.use('fivethirtyeight')
    fig = plt.figure(figsize=(16, 8))
    plt.subplots_adjust(left=0.04, right=1, top=0.929, wspace=0.145, hspace=0.152)
    ax1 = fig.add_subplot(2, 3, 1)
    ax2 = fig.add_subplot(2, 3, 2)
    ax3 = fig.add_subplot(2, 3, 3)
    indicators1 = fig.add_subplot(2, 3, 4)
    indicators2 = fig.add_subplot(2, 3, 5)
    indicators3 = fig.add_subplot(2, 3, 6)
    account = Account.Account()
    bought = {'1':0, '2':0, '3':0}

    def animate(i):
        #1st stock
        data = yf.download(tickers=tickers, period="1d", interval="1m", group_by='ticker')
        data = data.apply(pd.to_numeric, errors='coerce')
        data = data.dropna()
        ys1 = data[tickers[0]]['Adj Close']
        longMA1 = data[tickers[0]]['Adj Close'].ewm(span=100, adjust=False).mean()
        medMA1 = data[tickers[0]]['Adj Close'].ewm(span=50, adjust=False).mean()
        shortMA1 = data[tickers[0]]['Adj Close'].ewm(span=25, adjust=False).mean()
        current1 = ys1[-1]
        buy_strength1 = 0
        if current1 > longMA1[-1] and current1 > shortMA1[-1]:
            trend = "Strong Upwards trend"
            buy_strength = 2
        elif current1 > longMA1[-1]:
            trend = "Upwards trend"
            buy_strength = 1
        else:
            trend = "Downwards trend"
            buy_strength = 0
        xs = list(range(1, len(ys1)+1))
        ax1.clear()
        ax1.plot(xs, ys1, label='Stock Price', color='blue', linewidth=2)
        ax1.plot(xs, longMA1, label='Long Moving Average', color='red', alpha=0.7, linewidth=1)
        ax1.plot(xs, medMA1, label='Med Moving Average', color='orange', alpha=0.7, linewidth=1)
        ax1.plot(xs, shortMA1, label='Short Moving Average', color='yellow', alpha=0.7, linewidth=1)
        ax1.set_title("Stock: "+tickers[0]+" Current Price: " + "{:.2f}".format(ys1[-1])+"\nMovement: "+trend, fontsize=12)
        ax1.legend(loc='upper left', fontsize=8)

        shortEMA1 = data[tickers[0]]['Adj Close'].ewm(span=12, adjust=False).mean()
        longEMA1 = data[tickers[0]]['Adj Close'].ewm(span=26, adjust=False).mean()
        MACD1 = shortEMA1 - longEMA1
        signal1 = MACD1.ewm(span=9, adjust=False).mean()
        indicators1.clear()
        indicators1.plot(xs, MACD1, label='MACD', color='red', linewidth=1)
        indicators1.plot(xs, signal1, label='Signal', color='green', linewidth=1)
        indicators1.legend(loc='upper left', fontsize=8)
        indicators1.set_title("Indicators", fontsize=12)

        if bought['1'] == 0:
            if MACD1[-1] > signal1[-1] and MACD1[-2] < signal1[-2] and buy_strength > 0:
                if buy_strength == 2:
                    print("Strong ", end=" ")
                print("Buy Signal @ " + str(current1))
                shares1 = account.money / ys1[-1]
                account.buy_shares(current1)
                price_target1 = ((shares1 * current1) * 1.02) / shares1
                stop_loss1 = ((shares1 * current1) * 0.99) / shares1
                bought['1'] = 1

        if bought['1'] == 1:
            if MACD1[-1] < signal1[-1] and MACD1[-2] > signal1[-2]:
                account.sell_shares(current1, shares1)
                bought['1'] = 0

            if current1 <= stop_loss1 or current1 >= price_target1:
                account.sell_shares(current1, shares1)
                bought['1'] = 0


        # 2nd ticker
        ys2 = data[tickers[1]]['Adj Close']
        longMA2 = data[tickers[1]]['Adj Close'].ewm(span=100, adjust=False).mean()
        medMA2 = data[tickers[1]]['Adj Close'].ewm(span=50, adjust=False).mean()
        shortMA2 = data[tickers[1]]['Adj Close'].ewm(span=25, adjust=False).mean()
        current2 = ys2[-1]
        if current2 > longMA2[-1] and shortMA2[-1] > medMA2[-1] > longMA2[-1]:
            trend = "Strong Upwards trend"
            buy_strength = 2
        elif current2 > longMA2[-1]:
            trend = "Upwards trend"
            buy_strength = 1
        else:
            trend = "Downwards trend"
            buy_strength = 0
        xs = list(range(1, len(ys2) + 1))
        ax2.clear()
        ax2.plot(xs, ys2, label='Stock Price', color='blue', linewidth=2)
        ax2.plot(xs, longMA2, label='Long Moving Average', color='red', alpha=0.7, linewidth=1)
        ax2.plot(xs, medMA2, label='Med Moving Average', color='orange', alpha=0.7, linewidth=1)
        ax2.plot(xs, shortMA2, label='Short Moving Average', color='yellow', alpha=0.7, linewidth=1)
        ax2.set_title("Stock: " + tickers[1] + " Current Price: " + "{:.2f}".format(ys2[-1]) + "\nMovement: " + trend,
                      fontsize=12)
        ax2.legend(loc='upper left', fontsize=8)

        shortEMA2 = data[tickers[1]]['Adj Close'].ewm(span=12, adjust=False).mean()
        longEMA2 = data[tickers[1]]['Adj Close'].ewm(span=26, adjust=False).mean()
        MACD2 = shortEMA2 - longEMA2
        signal2 = MACD2.ewm(span=9, adjust=False).mean()
        indicators2.clear()
        indicators2.plot(xs, MACD2, label='MACD', color='red', linewidth=1)
        indicators2.plot(xs, signal2, label='Signal', color='green', linewidth=1)
        indicators2.legend(loc='upper left', fontsize=8)
        indicators2.set_title("Indicators", fontsize=12)

        if bought['2'] == 0:
            if MACD2[-1] > signal2[-1] and MACD2[-2] < signal2[-2] and buy_strength > 0:
                if buy_strength == 2:
                    print("Strong ", end=" ")
                print("Buy Signal @ " + str(current2))
                shares2 = account.money / ys2[-1]
                account.buy_shares(current2)
                price_target2 = ((shares2 * current2) * 1.02) / shares2
                stop_loss2 = ((shares2 * current2) * 0.99) / shares2
                bought['2'] = 1

        if bought['2'] == 1:
            if MACD2[-1] < signal2[-1] and MACD2[-2] > signal2[-2]:
                account.sell_shares(current2, shares2)
                bought['2'] = 0

            if current2 <= stop_loss2 or current2 >= price_target2:
                account.sell_shares(current2, shares2)
                bought['2'] = 0

        #3rd stock
        ys3 = data[tickers[2]]['Adj Close']
        longMA3 = data[tickers[2]]['Adj Close'].ewm(span=100, adjust=False).mean()
        medMA3 = data[tickers[2]]['Adj Close'].ewm(span=50, adjust=False).mean()
        shortMA3 = data[tickers[2]]['Adj Close'].ewm(span=25, adjust=False).mean()
        current3 = ys3[-1]
        if current3 > longMA3[-1] and shortMA3[-1] > medMA3[-1] > longMA3[-1]:
            trend = "Strong Upwards trend"
            buy_strength = 2
        elif current3 > longMA3[-1]:
            trend = "Upwards trend"
            buy_strength = 1
        else:
            trend = "Downwards trend"
            buy_strength = 0
        xs = list(range(1, len(ys3) + 1))
        ax3.clear()
        ax3.plot(xs, ys3, label='Stock Price', color='blue', linewidth=2)
        ax3.plot(xs, longMA3, label='Long Moving Average', color='red', alpha=0.7, linewidth=1)
        ax3.plot(xs, medMA3, label='Med Moving Average', color='orange', alpha=0.7, linewidth=1)
        ax3.plot(xs, shortMA3, label='Short Moving Average', color='yellow', alpha=0.7, linewidth=1)
        ax3.set_title("Stock: " + tickers[2] + " Current Price: " + "{:.2f}".format(ys3[-1]) + "\nMovement: " + trend,
                      fontsize=12)
        ax3.legend(loc='upper left', fontsize=8)

        shortEMA3 = data[tickers[2]]['Adj Close'].ewm(span=12, adjust=False).mean()
        longEMA3 = data[tickers[2]]['Adj Close'].ewm(span=26, adjust=False).mean()
        MACD3 = shortEMA3 - longEMA3
        signal3 = MACD3.ewm(span=9, adjust=False).mean()
        indicators3.clear()
        indicators3.plot(xs, MACD3, label='MACD', color='red', linewidth=1)
        indicators3.plot(xs, signal3, label='Signal', color='green', linewidth=1)
        indicators3.legend(loc='upper left', fontsize=8)
        indicators3.set_title("Indicators", fontsize=12)

        if bought['3'] == 0:
            if MACD3[-1] > signal3[-1] and MACD3[-2] < signal3[-2] and buy_strength > 0:
                if buy_strength == 2:
                    print("Strong ", end=" ")
                print("Buy Signal @ " + str(current3))
                shares3 = account.money / ys3[-1]
                account.buy_shares(current3)
                price_target3 = ((shares3 * current3) * 1.02) / shares3
                stop_loss3 = ((shares3 * current3) * 0.99) / shares3
                bought['3'] = 1

        if bought['3'] == 1:
            if MACD3[-1] < signal3[-1] and MACD3[-2] > signal3[-2]:
                account.sell_shares(current3, shares3)
                bought['3'] = 0

            if current3 <= stop_loss3 or current3 >= price_target3:
                account.sell_shares(current3, shares3)
                bought['3'] = 0

    ani = animation.FuncAnimation(fig, animate, interval=10000)
    plt.show()


def convert(lst):
    return ([i for item in lst for i in item.split()])

def print_menu():
    print("1. Enter list of tickers\n2. Start Analysis\n3. Exit")

if __name__ == '__main__':
    choice = '0'
    while choice != '3':
        print_menu()
        choice = input('Enter Selection: ')

        if choice == '1':
            tickers = [input('Enter tickers(3): ')]

        if choice == '2':
            ticker_list = convert(tickers)
            plot(ticker_list)

        if choice == '3':
            print("Closing.")
            time.sleep(1)
            print("Closing..")
            time.sleep(1)
            print("Closing...")
            time.sleep(1)

