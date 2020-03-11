Shinyuwu's work

The Final File is in TradingBot file.

## Prerequest

To set the environment: `$ pip install -r requirements.txt `

After installing the environment, open the `Trade.ipynb` and run the file.

If you want to test in real time, then run the `Real Time Trade.ipynb`

## Connect to Binance Account and trade

Under the `def buy(self, HA_close, HA_open,HA_high, HA_low, VIX_Close)`, comments off `client.order_market_sell(symbol = 'BTCUSDT',quantity = sell_units)` and `client.order_market_buy(symbol = 'BTCUSDT',quantity = buy_units)`



## Trading Bot

![Trading](https://github.com/svelte-studios/BitBotBoom/blob/master/shinyuwu/img/Trading.png)

The framework of the trading bot:

![Fig_TradingBot](https://github.com/svelte-studios/BitBotBoom/blob/master/shinyuwu/img/Fig_TradingBot.png)



I am using the evolution strategy and reinforcement learning to train the trading bot.

- Agent - Trading bot itself.
- State -  Every time when the new data comes in, the state will change. The agent will take action according to the state.
- Reward - The goal of the agent is to get the maximize rewards.



## About Evolution Strategy

The method of evolution strategy is jittering the noise on weights, I set 25 population in `Agent.py`, which means these 25 workers will walk in different directions (noise), and take different actions under different state. After traing 300 epochs, the agent will learn from previous experience, and take the best action on the testing time.



## Trading Strategy

- You have two ways to start the trade:

  1) **Agent decide the first buy point**- set initial money and let the agent to trade, which means the start trade point for the machine is '*buy point*'
  2) **You decide the first buy point-** you buy the bitcoin in advanced, and let the agent to trade, which means the start trade point for the machine  is '*sell point*'.

- Use **All** the money to buy the bitcoin, and when the sell point comes, sell **All** the bitcoin you have.

- Commission rate: 

  We found use BNB coin (another kind of crypto currency) to pay the the commision rate is the most cost saving. Here is the formula to calculate the commossion fee:

   `0.001x 0.75x BTC transaction price; unit: BNB coin`

- Indicators:

  

  - **VIX**
  
    The fear index. I catch the vix trend as selling signal. When the vix raise over a threshold, the agent will directly sell the bitcoin.
    
    I've done the XGBoost to test the feature importances among sevral factors. Since VIX has high XGBoost score and the trend is contrast to BTC price, I appy VIX as a selling point signal.
    
    ![VIX and BTC Price](https://github.com/svelte-studios/BitBotBoom/blob/master/shinyuwu/img/VIX.png)
  
  - Heiken Ashi
  
    **Now I've removed heiken ashi as a buy signal indicator, but just incase, I still preserve the code. You can skip this indicators**
  
    I try to find some insight from the candlestick and detect the best buy point. Using Heiken Ashi to plot the candlestick would be more stable. So I apply this method into the model:
  
    - Buy Signal: I found befor the price raise up, there is a signal looks like this one: The green candle with upper wick and without tail wick. So when the signal shows, the agent will buy bitcoin if it has money.
      ![Heiken Ashi](https://github.com/svelte-studios/BitBotBoom/blob/master/shinyuwu/img/Buy_Signal.png)
  
  
  
  
  
  
  
  

