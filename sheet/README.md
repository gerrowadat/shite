# sheet - a cli thing for messing with google sheets


This doesn't do much currently, aside from pulling csv data from sheet ranges.

```
sheet get SpReAdShEeTiDfRoMUrL 'myworksheet!B3:F8'
...
```

See `sheet help get` for flags, you'll need a client secret file, per the docs.

TODO:

```
# Reading
sheet head/tail <id> <worksheet>

# Writing
sheet put <id> <datarange>
sheet replace/append <id> <worksheet>

# Etc.
sheet touch
sheet rm
sheet ls
sheet cp
```