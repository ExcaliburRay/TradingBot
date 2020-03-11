import datetime as dt
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
import random
import matplotlib.dates as mdates
import math
import pandas as pd
import numpy as np
from plotly import __version__
from plotly import graph_objs as go
from binance.client import Client
from Deep_Evolution_Strategy import Deep_Evolution_Strategy

class Agent:

    POPULATION_SIZE = 25
    SIGMA = 0.1
    LEARNING_RATE = 0.03
    skip = 1

    def __init__(self, model, close, time,money, btc, btcPrice, bnbCoin):
        self.model = model
        self.close = close
        self.time = time
        self.initial_money = money
        self.btc = btc
        self.btcPrice = btcPrice
        self.bnbCoin = bnbCoin
        self.es = Deep_Evolution_Strategy(
            self.model.get_weights(),
            self.get_reward,
            self.POPULATION_SIZE,
            self.SIGMA,
            self.LEARNING_RATE,
        )

    def get_state(self, data, t, n):
        d = t - n + 1
        block = data[d : t + 1] if d >= 0 else -d * [data[0]] + data[0 : t + 1]
        res = []
        for i in range(n - 1):
            res.append(block[i + 1] - block[i])
        return np.array([res])


    def act(self, sequence):
        decision = self.model.predict(np.array(sequence))
        return np.argmax(decision[0])

    def get_reward(self, weights):
        '''
        In order to make the agent learn in a more efficient way, 
        when the agent make mistake, I set a large amount of punishment to make the reward become minus, 
        whereas if it sell at a good point, I add a high reward.

        '''
        initial_money = self.initial_money
        btc = self.btc
        btcPrice = self.btcPrice
        starting_money = initial_money
        self.model.weights = weights
        close = self.close
        l = len(close) - 1
        window_size = 51
        state = self.get_state(close, 0, window_size + 1)
        inventory = []
        if btc >0 :
            inventory.append(btc)
            initial_money = 0
            total_buy = btcPrice
            starting_money = btcPrice
            quantity = btc
        else:
            inventory = []
            quantity = 0
        for t in range(0, l, 1):
            action = self.act(state)
            close = self.close
            next_state = self.get_state(close, t + 1, window_size+ 1)
            if action == 1 and initial_money >=1:
                buy_units = self.round_down(initial_money/close[t+1],8)
                total_buy = buy_units * close[t+1]
                initial_money -= total_buy
                initial_money -=  10
                inventory.append(total_buy)
                quantity += buy_units
            elif action == 2 and len(inventory) > 0 and (close[t+1]*quantity)>=(total_buy):
                sell_units = quantity
                quantity -= sell_units
                total_sell = sell_units * close[t+1]
                initial_money += total_sell
                initial_money -= 10
            # Add punishment
            elif action == 2 and len(inventory) > 0 and (close[t+1]*quantity)<(total_buy):
                sell_units = quantity
                quantity -= sell_units
                total_sell = sell_units * close[t+1]
                initial_money += total_sell
                if (close[t+1]*quantity)<=(total_buy*0.97):
                    initial_money -= 30   # punishment
                else:
                    initial_money -= 10
            state = next_state
        return ((initial_money - starting_money) / starting_money) * 100

    def fit(self, iterations, checkpoint):
        self.es.train(iterations, print_every = checkpoint)

    def round_down(self, value, decimals):
        factor = 1 / (10 ** decimals)
        return (value // factor) * factor

    def buy(self, HA_close, HA_open,HA_high, HA_low, VIX_Close):
        api_key = 'ddeCyGpnkF2rrO0NyzFjjzFD6fWL4LDurf1e704GqkWck20V777VvxBNUSJkFGmP'
        api_secret = 'oZNSUX3f5Sltzr9KJBkNng8rA5hc14sV45ufNczM5MSRWFMmGcpXcQF6j0dZEkeU'

        client = Client(api_key, api_secret, {"verify": False, "timeout": 20})
        initial_money = self.initial_money
        btc = self.btc
        btcPrice = self.btcPrice
        bnbCoin = self.bnbCoin
        close = self.close
        time = self.time
        window_size = 51
        state = self.get_state(close, 0, window_size + 1)
        self.HA_close = HA_close
        self.HA_open = HA_open
        self.HA_high = HA_high
        self.HA_low = HA_low
        self.VIX_Close = VIX_Close
        l = len(close) - 1
        starting_money = initial_money
        states_sell = []
        states_sell_price = []
        states_buy = []
        states_buy_price = []
        inventory = []
        sellVIX = []
        BNBtoUSD = 17 
        ## Assume 1 BNB coin worth 17 USD dollar.

        if btc >0 :
            inventory.append(btc)
            initial_money = 0
            total_buy = btcPrice
            starting_money = btcPrice
            quantity = btc
        else:
            inventory = []
            quantity = 0
        signal_time = []
        signal_shows = []
    
        for t in range(0, l, 1):
            action = self.act(state)
            next_state = self.get_state(close, t + 1, window_size + 1)
            signal_time.append(t)

            # Add Sell signal     
            if quantity> 0.000000 and bnbCoin >0 and VIX_Close[t+1]- VIX_Close[t] >= 1.2 and (close[t+1]*quantity-total_buy)>=(-total_buy*0.1): 
            #and HA_open[t+1]-HA_close[t+1]>50 and 0.4<= ((HA_close[t+1]-HA_open[t+1])/(HA_low[t+1]-HA_open[t+1]))<=0.75:
                sellVIX.append(1)
                bought_price = inventory.pop(0)
                sell_units = quantity
                quantity -= sell_units
                total_sell = sell_units * close[t+1]
                bnbCoin -= 0.001*0.75*total_sell/BNBtoUSD
                initial_money += total_sell
                initial_money -= total_sell*0.001*0.75
                states_sell.append(time[t+1])
                states_sell_price.append(close[t+1])
                signal_shows.append(2)
                try:
                    invest = ((total_sell - bought_price) / bought_price) * 100
                except:
                    invest = 0
                print(
                    'time %d, sell %f units at price %f, investment %f %%, total balance %f,BNB coin %f'
                    % (t+1, sell_units, close[t+1], invest, initial_money,bnbCoin)
                )
                
                print('Sell because of VIX')
                client.order_market_sell(symbol = 'BTCUSDT',quantity = sell_units)
                continue
            else:
                sellVIX.append(0)

            if action == 1 and initial_money >=1 and bnbCoin >0 and sellVIX[t-1]== 0 and sellVIX[t]== 0:
                if t >= 2:
                    if sellVIX[t-2]== 1:
                        continue
                buy_units = self.round_down(initial_money/close[t+1],8)
                total_buy = buy_units * close[t+1]
                bnbCoin -= 0.001*0.75*total_buy/BNBtoUSD ######### BNB to USD = 17
                initial_money -= total_buy
                initial_money -= total_buy*0.001*0.75
                inventory.append(total_buy)
                quantity += buy_units
                states_buy.append(time[t+1])
                states_buy_price.append(close[t+1])
                signal_shows.append(1)
                print(
                    'time %d: buy %f units at price %f, total balance %f,BNB coin %f'
                    % (t+1, buy_units, close[t+1], initial_money,bnbCoin)
                )
                client.order_market_buy(symbol = 'BTCUSDT',quantity = buy_units)
#                 status.append('buy')
            elif action == 2 and len(inventory) > 0 and (close[t+1]*quantity)>=(total_buy+1.5) and bnbCoin >0:
                bought_price = inventory.pop(0)
                sell_units = quantity
                quantity -= sell_units
                total_sell = sell_units * close[t+1]
                bnbCoin -= 0.001*0.75*total_sell/BNBtoUSD
                initial_money += total_sell
                initial_money -= total_sell*0.001*0.75
                states_sell.append(time[t+1])
                states_sell_price.append(close[t+1])
                signal_shows.append(2)
                try:
                    invest = ((total_sell - bought_price) / bought_price) * 100
                except:
                    invest = 0
                print(
                    'time %d, sell %f units at price %f, investment %f %%, total balance %f, BNB coin %f'
                    % (t+1, sell_units, close[t+1], invest, initial_money,bnbCoin)
                )
                client.order_market_sell(symbol = 'BTCUSDT',quantity = sell_units)
            else:
                signal_shows.append(0)
            state = next_state


        invest = ((initial_money - starting_money) / starting_money) * 100
        print(
            '\ntotal gained %f, total investment %f %%'
            % (initial_money - starting_money, invest)
        )

        fig = go.Figure()
        fig.add_trace(go.Scatter(x = time,y=close,
                    line=dict(color='silver', width=2),
                    mode='lines',
                    name='close price'))
        fig.add_trace(go.Scatter(x = states_sell,y=states_sell_price,
               line=dict(color='firebrick',width=1),
                mode='markers', name='sell point'))
        fig.add_trace(go.Scatter(x = states_buy,y=states_buy_price,
                    mode='markers', name='buy point'))  
        fig.show()

