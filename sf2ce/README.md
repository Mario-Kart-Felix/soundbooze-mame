# Street Fighter II: Champion Edition (sf2ce)

Various Reinforcement Learning methods for Street Fighter II: Champion Edition

(Under development)

### Version

World 920513

![alt text](https://raw.githubusercontent.com/soundbooze/soundbooze-mame/master/sf2ce/obsolete/sync/noise/sf2.png "sf2ce")

### Reposition

- Launch mame | (for multi-training use composite window) **

** need more scalabe-solution

```
$ ../reposition.sh
```

## Random Agent

Fully Random Agent 

```
$ sleep 2 && python stream.py
```

## Feed

Random exploration while preserving-serufulness

- vs Machine

```
meth: {lr.py, shift.py}
$ sleep 2 && python $meth
```

- P1 vs P2

```
$ sleep 2 && (python shift.py | python lr2.py)
```

- Stage Rehearsal

Load stage, choose P1 | P2

```
$ sleep 2 && python (cd pg/ && play.py | python lr2.py)

```

## Policy Gradient

- Timestep (Policy Gradient)

pg/

### Play

```
$ python play.py
```

## Spin Imitate Reverse

hb/ sir/ hybrid/

(Under work)

## Continuous-States Q Learning

Q/ [under-development]

- dipikir-LAN-nurut problem, similar/same state doesn't guarantee similar reward
- variable-naming-convention *won't hellp much
- long/lat arrival labeling|measuring  --* too (mbrojol-on-arrival)
- forced-reward-penalty injection

### Play

```
$ python main.py $1
```

- $1 (target directory)

### Resume

```
$ python main.py $1 $2
```  

- $1 (target directory)
- $2 (HQ pickle filename)

### Display Plot

```
$ python show $1
```

- $1 (HQ pickle filename)

## License

UDUK™ Free as an AIR License
