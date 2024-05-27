mkdir -p _site/recurse
mkdir -p _site/recurse/css

# generate directory structure for dagzet
find data/* -type d | sed "s/^data\///" | xargs -I {} mkdir -p _site/recurse/dz/{}

# task management
mkdir -p _site/recurse/tasks
mkdir -p _site/recurse/taskgroups

weewiki sync
weewiki export
rsync -rvt css/style.css _site/recurse/css
