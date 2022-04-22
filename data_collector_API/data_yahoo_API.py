'''
stock trend analyzer, save any findings for frequencies etc.
WHAT IS MY GOAL?
 1) Turn the SP500 into the default growth of market
    1.1) Plot regression line of SP500
    1.2) Use SP500 as the "base line" to compare other markets
 2) with the two types of data above, FFT to find frequency spikes! 
 3) Change the type of data i'm analyzing:
    3.1) how many days
    3.2) average days
    3.3) what number to grab?

 -  goal when i come back: plot the fft of the SP500 normal, 
    see if the market has any hidden trends
'''

import ftplib
import io
from xml.etree.ElementTree import XML
import pandas
import numpy as np
from matplotlib import pyplot as plt
import requests
import requests_html
from yahoo_fin.stock_info import get_data
import datetime
from scipy.fftpack import fft, ifft
# from numpy.fft import fft, ifft


##### global stuff 
regression_line_path = r'C:\Users\DeanTheBean\Dean_Main\UCLA_migrate_201118\Dean_Transfer\Work\Stocks\regression'




def date_plug(y):
    #First grab today's date to past 5 years for analysis
    formatted_date = datetime.date.strftime(datetime.date.today(), "%m/%d/%Y")
    date = int(formatted_date[6:] ) - y
    formatted_date_y = formatted_date[:6] + str(date)
    # formatted_date_y = "04/20/2020" #hard coded covid start
    return formatted_date_y, formatted_date  

def smooth_curve(x_np, n):
    smooth = []
    pos = 0
    for val in x_np:
        if pos >= n:
            total = 0
            for i in range(n+1):
                total += x_np[i - n + pos]
            smooth.append(total/(n+1))
        else:
            smooth.append(sum(x_np[:pos])/(pos+1))
        pos += 1

    return smooth



def plot_freq(stock_list, plt_name, smooth):
    show_plot = 1
    save_plot = 1
    line_plot = 0
    fft_plot = 1
    x, true_norm_list = get_true_norm(stock_list)
    smooth_true_norm_list = smooth_curve(true_norm_list, smooth)

    if line_plot:
        plt.plot(x, smooth_true_norm_list)
        plt.title(plt_name)

    if fft_plot:
        X = fft(smooth_true_norm_list)
        N = len(X)
        n = np.arange(N)
        # get the sampling rate
        sr = 1
        T = N/sr
        freq = n/T 
        # print(freq)
        n_oneside = N//2
        f_oneside = freq[:n_oneside]
        freq_list = np.abs(X[:n_oneside])
        print(max(freq_list))
        
        plt.figure(figsize = (12, 6))
        plt.title(plt_name)
        plt.plot(f_oneside, freq_list, 'b')
        plt.xlabel('Freq (Hz)')
        plt.ylabel('FFT Amplitude |X(freq)|')
        
    if save_plot: plt.savefig('%s/%s_%s.png' % (regression_line_path, plt_name, str(smooth)))
    if show_plot: plt.show()
    # plt.close()



def get_true_norm(n): #make 
    first_price, true_norm_list, x1 = n[0], [], []
    normal_list_1 = [round(d/first_price, 3) for d in n] #get norm to 1
    for i in range(0, len(normal_list_1)): x1.append(i)
    x = np.array(x1)
    normal_list = np.array(normal_list_1)
    m, b = np.polyfit(x, normal_list, 1) #get slope and intercept
    for idx, nl in enumerate(normal_list_1): true_norm_list.append(round(nl-(m*idx + b),2))
    return x, true_norm_list




def data_select(smooth_factor, years, ticker_price_option):
    starting, ending = date_plug(years)
    historical_datas = {}
    for ticker in ticker_list:
        historical_datas[ticker] = get_data(ticker, 
        start_date= starting, end_date= ending, interval="1d")

        # if ticker_price_option == ''



        
        list_of_names = historical_datas[ticker]["close"].to_list()
        
        plot_freq(list_of_names, ticker, smooth_factor)

# ticker_list = ["amzn", "aapl", "tsla", "voo", "gpk", "brk-b", "GOOGL.MI", "TH"]
# ticker_list = ["voo", "aapl", "tsla", "gpk", "brk-b", "GOOGL.MI"]
# ticker_list = ["voo", "aapl"]
ticker_list = ["aapl"]

def main():

    smooth_factor = 60
    years = 10

    data_select(smooth_factor, years, 0)
























if __name__ == '__main__':
    main()