# STONKS
Stonks is a unique stock market simulation game made for the Kamand Premier League by E-Cell, IIT Mandi. The motive of the game is to create an environment where players have to bet on the knowledge of their teammates and opponents in order to earn maximum profit by the end of the game. Each player except the team leaders is assigned a predetermined initial value(in this case, we have used the auction prices from the beginning of KPL) and this value changes depending on the performance of the player through the game. Team leaders, on the other hand, are the investors who have the ownership of the stocks of their teammates and some currency to buy shares from the stocks of opponent team players. As a result the change in the value of a player affects the wealth of all of his/her stakeholders and not only his team’s leader. To make the game fair, every team will start with an equal net wealth(currency+stock).
[More details](https://docs.google.com/document/d/1uSCBedBDyrKK11zIe8qKrfJOPGdqICBzwVm2w-ePUGU/edit?usp=sharing)

## STONKS-automation-scripts
Python scripts for partially automating game's google sheet for keeping record.

1. **ipo:** Complete implementation of IPO round proceedings. Enter the locked players(not for sale) of each team. Enter the buying wishlist of each team and trading will be done automatically.

1. **quiz:** Run at the start of each quizzing round. Each team nominates 3 players and the script randomly chooses one from each team for each question. Keep entering names of players who respond to the question along with their response(1/0).

1. **trade:** Enter the details of a trade during trading round in the given format to update the share values and currency balance of involved parties.

## Web Application
Will be adding a server side implementation of all the scripts in node.