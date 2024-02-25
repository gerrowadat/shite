# sheet - a cli thing for messing with google sheets


Insert under construction gif here.

Stuff that currently (sort of) works:

```
# Set $SHEET_CLIENTSECRET_FiLE and $SHEET_TOKEN_FILE to your client secret json file and oauth token file respectively.
# Or pass --clientsecretfile and --authtokenfile to the following:

# Get a range and spit it out as CSV
sheet get SpReAdShEeTiDfRoMUrL 'myworksheet!B3:F8'

# Print the last 5 populated rows of a worksheet
sheet tail SpReAdShEeTiDfRoMUrL 'myworksheet' 5

# List the worksheets in the specified sheet
sheet ls SpReAdShEeTiDfRoMUrL 
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
sheet cp
```