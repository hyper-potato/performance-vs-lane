# performance-vs-lane  
Concise but Not so concise analysis[on my blog](https://hyper-potato.github.io/2020/02/29/Swimmer-Performance-vs-Lane-Placement/)
**Lane Placement and Performance: A Causal Exploration**  
<br/>
The question that we are hoping to answer in our final project of Causal Inference is whether there is a causal effect of lane placement upon the performance of competitive swimmers. More specifically, we want to assess whether being in a lane closer to the center of the pool gives a competitive edge. There is great debate in the swimming world if outside lanes are put at a disadvantage, but prior studies have produced conflicting results.
<br/><br/>
An ideal experiment to test this hypothesis would require several steps. First, a sufficiently large group of swimmers in a specific race would have to be gathered. Then, they should be randomly assigned to lanes and race following a day with a consistent routine and warmup across the subjects. Regression analysis could then be performed to assess whether lane placement has a causal effect on speed.
<br/><br/>
Using an observational study would certainly be more practical, however, it comes with some clear threats to causal inference.  <br/><br/>
First, we have an issue of simultaneity in the form of reverse causality. Typically, lane placement is based on either a seed time or a prelims time with faster swimmers being placed in more central lanes. To combat this, we hope to examine swimmers who swam in both prelims and finals of a meet and compare the change in speed with change in lanes.
<br/><br/>
Another threat we may face in an observational study would be selection bias. It may be quite hard to get a truly random sample and our results may not be generalizable past championship meets (those having both prelims and finals of events). 
<br/><br/>
Finally, we may see some omitted variable bias that we cannot control for. For example, various factors such as training routine, age, suit worn, and others are likely correlated with a change in time. However, these may not be correlated with a change in lane.


