# jeans
An exploration of [multi-level selection][0] (group selection) by simulation with a genetic algorithm and deep learning in Python.

The goal of this repository is to better understand this weird concept known as "group selection" by programming an evolutionary simulation with groups that are in competition with each other and the members of each group can choose to cooperate with their groupmates or not. Hopefully, altruism will emerge, but I am also unsure of the fundamental parts of biology that I misunderstand. So that's another goal: to learn what I don't know about biology by blindly simulating a small piece of it. 

## Inspirational Readings
* [Sapiens][1] by Yuval Noah Harari - particularly chapter 2
* [The Righteous Mind][2] by Jonathan Haidt - particularly [chapter 9][3] and [this lecture][4]
* [Up and Down the Ladder of Abstraction][6] by Bret Victor

## Tools
* Pymunk - physics engine
* Pyglet - game/visualization library
* Numpy - multi-dimentional math library
* Keras - deep learning library

## Running The Simulation
Make a Python virtual environment
```
python3 -m venv venv
```
Run the virtual environment
```
source venv/bin/activate
```
Install all of the requirements
```
pip install -r requirements.txt
```
Enter [the matrix][5]
```
python3 sim.py
```

[0]: https://en.wikipedia.org/wiki/Group_selection#Multilevel_selection_theory
[1]: https://en.wikipedia.org/wiki/Sapiens:_A_Brief_History_of_Humankind
[2]: https://en.wikipedia.org/wiki/The_Righteous_Mind
[3]: https://www.righteousmind.com/wp-content/uploads/2012/08/RighteousMind.Chapter-9.pdf
[4]: https://youtu.be/NQ192d4c4S0
[5]: https://en.wikipedia.org/wiki/The_Matrix
[6]: http://worrydream.com/LadderOfAbstraction/
