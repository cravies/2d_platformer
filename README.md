# Game
Making a 2d platforming game to keep my development skills sharp as my studies this semester are mostly focused on networking/security stuff. Currently a basic version is working. Need to make some art for it and come up with a story. It's also kind of slow so I will do some optimizations at some point.

To play the game:

```Bash
python3 game.py
```

To run the level editor:

```Bash
python3 gui.py
```

Game description:
The goal of the game is to reach the other side of the screen as many times as you can without dying. Each time you reach the other side of the screen, the map with randomly change slightly, up to 10 times, at which point you will be transported to the next level. Along the way you should avoid enemies. If you jump on them, they will die. If you want to break blocks in from of you, you can do that using the dig mechanic.

Left/right: normal left/right directional keys
Jump: spacebar
Dig: up 


TODO: Game Engine

- [ ] Nice looking physics for when player jumps on enemy
- [ ] Save game
- [ ] Game over screen: "try again" / "quit"
- [ ] Level complete condition 

TODO: Design

ART for:
- [ ] Player: static
- [ ] Player: moving
- [ ] Player: hurt
- [ ] Enemies: static
- [ ] Enemies: moving
- [ ] Enemies: hurt
- [ ] Background

DESIGN:
- [ ] Level 1
- [ ] Level 2
- [ ] Level 3
- [ ] Level 4
- [ ] Level 5
- [ ] Level 6
- [ ] Level 7
- [ ] Level 8
- [ ] Level 9
- [ ] Level 10
