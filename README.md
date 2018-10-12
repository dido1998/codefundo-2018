# codefundo-2018
The official repo of team flow.

We will focus on floods currently, we may add support for other disasters-

## Problems
We think that there is lack of coherency in fighting floods and running relief operations. We want to solve this problem by providing a communication interface between the NGOs (or government) and the general public. We want to help run more organised relief operations. Recently we were hit by the Kerela floods and one thing we observed that people were posting about their situation on twitter but a lot of their pleas were going un-noticed. For example here are a few example tweets that most likely went un-noticed or were noticed to late-
```
Respected Defence Minister, please check Malayalam news about Chengannur MLA's (Saji Cheriyan) plea for exclusive army and airlift support. He fears a huge death toll if help is not provided soon. Pls provide max help. @DefenceMinIndia @nsitharaman @adgpi #OpMadad #KeralaFloods

"Kindly, provide us with a chopper..I am pleading you.Please help us.Otherwise, my people will die"
```
This shows that most of the data is available online, we just have to organise it and use it. With all the data organised in one place,we can also come up with vastly more effecient relief routed to facilitate faster relief opeartions. This can be done by using basic algorithms once we have the correct coordinates.


## Solutions
Our solution is aimed at smartly organising data from online sources to make most use of it.

Our idea will be divided into the following parts-
- Our map will be for two sets of users- NGOs running relief operations and people stuck in flood 
- Extracting real-time maps of roads from an online API.
- Comparing pre-flood and post-flood images to detect flooded road by creating a road-segmentation network.
- NGOs will have access to the coordinates and the situation of people stuck in distress which will be extracted from twitter using the location API and sentiment analysis techniques. 
- The people stuck in floods can get updates about relief operations and send distress calls which include their location and situation.
- The location of the people will be used in formulating smart and effecient relief routes.

We plan to implement a chatbot interface to make the app more user friendly. People will also be able to communicate with the app using speech to text. We will also add an urgent distress button to signify the need for urgent help.
