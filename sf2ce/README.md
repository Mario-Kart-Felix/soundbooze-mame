# Street Fighter II: Champion Edition (sf2ce)

Various Reinforcement Learning methods for Street Fighter II: Champion Edition

### World 920513

![alt text](https://raw.githubusercontent.com/soundbooze/soundbooze-mame/master/sf2ce/obsolete/sync/noise/sf2.png "sf2ce")

### Reposition

- Launch mame

```
$ ../reposition.sh
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

## Policy Gradient

pg/

### Play

```
$ python play.py
```

## Q Learning

Q/ [under-development]

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
