Ray's work

It is a trading bot which implemented by five methods
1. MACD -- Buy at the Golden Cross, Sell at the Death Cross
2. Heikin-Ashi -- Buy when the color change into red;Sell when the color change into green
3. Heikin-Ashi (advanced) -- Ignore the effects of tiny candles change based on Heikin-Ashi Only
4. Heikin-Ashi plus MACD Signal Line -- Buy when the golden cross happen at the bullish trend, Sell when the death cross happen at the      bearish trend
5. Heikin-Ashi plus MACD Histogram -- performance almost similar with method four

After running all files like the above name, we could conduct the buy and sell point in the user-defined time range and time interval. If you want to make the trading bot in real-time version, you need to de-comment one code "time.sleep(30)".

API connection file is used to connect with emotion and subject API in Svelte

Email Notification file is used to send notifications when the system catches the buy and sell points. If you want to use this function, you need to create one CSV file and put your email address, password, the sending address into it.

Trading Strategy Comparison is used to compare the performance between four methods except for Heikin-Ashi plus MACD Signal Line. The result displays the most reasonable strategy is using Heikin-Ashi plus MACD Histogram at 4h time interval. 

Real Time is used to processing the real-time trading

