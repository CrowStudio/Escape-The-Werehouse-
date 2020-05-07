## Install the Game 

- Download the blob and extract it in a location of your choice.
- Install Python and/or PyGame 
	PyGame requires Python; if you don't already have it, you can download it from python.org.
	Use python 3.7.7 or greater, because it is much friendlier to newbies, and additionally runs faster.

	The best way to install PyGame is with the pip tool (which is what python uses to install packages).
	Note, this comes with python in recent versions.
	We use the --user flag to tell it to install into the home directory, rather than globally.
	```python
	python3 -m pip install -U pygame --user
	```

	To see if it works, run one of the included examples:
	```python
	python3 -m pygame.examples.aliens
	```

	If it works, you are ready to go!
	If not, more platform-specific instructions can be found here: https://www.pygame.org/wiki/GettingStarted

To run the game type:
```
python escape_the_warehouse.py
```
