## Slippi Scatter 
Generate a GIF of a Super Smash Bros Melee match using data from a slippi file.   

### Background & Synopsis
Slippi is an online matchmaking tool built by Fizzi and found here: https://slippi.gg/. It uses rollback netcode and saves replays to .slp files that can be later analyzed.

With this data, we can extract the x, y positions of players, along with damage information and plot them with Python. Using scatter plots, a match can be recreated and visually represented in a unique new way.  

### Requirements & Packages
* Python 3.7+ (tested on 3.11)
* Set up venv then: $ pip install -r requirements.txt 

### Example: Zain Vs. Jmook Game 4, Shine 2022 Grand Finals
Characters are represented by the solid circles while the damage taken represented by the expanding bubbles. The connecting line shows how each player is oriented to the other. 

<img src="Output/zain_jmook_g4_Shine2022_GFs.gif" alt="Aw Yeah" width="500">

### Known Issues
Slippi data changes over time with updates, some files require additional tinkering with the main function when extracting target player data. 
