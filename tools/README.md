# Tools
Various ad-hoc tools I've written in the past for workflow
and organization.

## evparse.sh

evparse parses a text file formatted using the event
log format. This is mostly a used as a data validator.

```
$ ./tools/evparse.sh logs/000_setup.txt
```

## dagzet

Used to parse out files written in the dagzet markup
language. Produces SQLite commands. Can also be used
to validate.

```
$ ./dagzet knowledge/workflow_planning.dz
```
