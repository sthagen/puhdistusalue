# Example Usage

Folder with only distinct files (normal mode):
```
$ puhdistusalue tests/fixtures/timestamps/all_distinct
removed 0 total redundant objects or 0 total bytes from folders at ['tests/fixtures/timestamps/all_distinct']
```

Folder with only distinct files and calling the module's main function per python (debug mode):
```
$ PURGE_RANGE_DEBUG=YES python -m puhdistusalue tests/fixtures/timestamps/all_distinct
KEEP file 20210508T111730.integer
KEEP file 20210508T111757.integer
KEEP file 20210508T111821.integer
KEEP file 20210508T111830.integer
KEEP file 20210508T111853.integer
removed 0 total redundant objects or 0 total bytes from folders at ['tests/fixtures/timestamps/all_distinct']
```
