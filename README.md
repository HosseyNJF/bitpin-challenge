# Bitpin Challenge

This is a coding challenge for *Bitpin* company.

## How this platform deals with fake ratings?

### The problem
A common problem with blogs is "rating attacks". It happens when an organized group of people attempt to manipulate an
article's rating by submitting fake ratings in bulk. Here's my take at mitigating this problem:

### The analysis

We need to define the characteristics of this kind of attacks in the first place, to be able to detect it.
- Most of these ratings would come from **new accounts**
- The attacks happen in a span of **1 to 2 days** 
- All the fake ratings have the same value - usually zero or five
- The rating vastly differs from the previous average rating - because there would be no point in an attack if it didn't
  impact the score of the article

We need to make sure that our solution doesn't impact the **organic ratings** and adheres to these requirements:
- The system should allow for an actual change of rating - we can't just ignore ratings that differ from the average as
  eventually there may be enough trustworthy ratings to organically change the average
- There needs to be a distinction between an attack and an actual, prolonged increase of rating volume that could come
  from sources like marketing campaigns and internet virality

It can be derived from these requirements and definitions that it's an extremely complicated problem to solve with a 
100% accuracy, as any mitigation method will eventually have some collateral damage to organic ratings due to attacks 
not having any easily distinguishable features from organic rates. Because of this, the solution must be configurable in
order to allow easy modification of trade-offs and strictness.

Also, due to the complexity of this problem, solutions can easily grow out of control and get too complex and 
unmaintainable. Simplicity, accuracy, and high performance are the main concerns and the following solutions are
designed with these properties in mind.

### The solution

Possible mitigations can work from multiple perspectives and angles. Here is a list of methods used in this project: 

#### User reputation
As mentioned in the attack characteristics, most of the fake ratings will come from accounts that have just been created
and/or have no previous ratings on any article. However, in case of a genuine prolonged increase in ratings, there will
be a lot of new accounts and their rating shall be considered more impactful.

In this method, all ratings that come from users that have registered in the past 3 days (configurable) or users with no
rating history will have a decreased weight that's affected with a configurable multiplier. The weight would be 
decreased even more if the value differs from the mean value. This will allow new users to have impact on article ratings 
if their rating is close to what the article already had (this is the collateral - new users cannot drastically change the rating).

This is the formula used to calculate the final weight of the rating of a new user between 0 and 1:


```
m = mean(article_ratings)
weight = "Constant Multipler Between 0 and 1" * (6 - abs(user_rating_value - m)) / 5
```

<sub>
An alternative would be to consider the account age and count of rating values directly in the formula. However,
in order to keep it simple, I chose to use a simple configurable condition instead.
</sub>

#### Detecting spikes - sudden changes in rating throughput
The user reputation method will prevent the more simple and low volume attacks. But attackers will learn that behaviour 
and can prepare a pool of high reputation fake users.

However, all attacks have one unique feature: They impact the amount of rating/hour significantly. By analysing this 
data, the fake reviews can be detected by checking if their timestamp is in the time interval that the attack happened.

This method will result in collateral damage to the genuine ratings that also happened in the timestamp of the attack,
but considering that the throughput has to be significantly changed in order for this mechanism to be triggered, it's 
safe to assume that most of the filtered out ratings were in fact fake. 

The threshold that triggers this mechanism is calculated by this formula:

```
timeframe = [3 days ago, 1 day ago]

threshold = mean(rate[timeframe]) + 2 * SD(rate[timeframe])
```

Both the timeframe and the standard deviation multiplier are configurable.

The weight that would be applied to the data points that happened in the attack period are calculated using this formula:

```
timeframe = [3 days ago, 1 day ago]
m = mean(values[timeframe])
weight = "Constant Multiplier Between 0 and 1" * (6 - abs(value - m)) / 5
```
