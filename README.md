# Research 
How long do the eye track changes need to impact the trust level?

![heatmap](./_generate_animation.gif)
[figure link](https://github.com/Mirandayao0/Research/blob/main/_generate_animation.gif)


The gif shows the trust changes of AI during the switch time from game panel to detecting panel.
1. check distribution -- know the range of heatmap
2. loop over eye1.txt to check time stamp, eye tracking coordinate,and confidence level
3. loop over toggle out.csv to check panel switch time, exam the duration of trust changes
start time: trust AI ,didn't switch to panel, end time: not enough trust, switch to panel to check enemy by himself
4. find overlap time,during the eye location changes, how confidence level changes, this reveal the trust on AI


```



