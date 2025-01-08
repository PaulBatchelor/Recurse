mkdir -p _site/recurse
mkdir -p _site/recurse/css

# generate directory structure for dagzet
# find data/* -type d | sed "s/^data\///" | xargs -I {} mkdir -p _site/recurse/dz/{}
while read -r line
do
    DATA_PATH=$(echo $line | cut -d ':' -f 1)
    mkdir -p _site/recurse/dz/$DATA_PATH
done < data_keys

echo "SELECT distinct(filename) from dz_textfiles" | sqlite3 a.db | xargs -I {} mkdir -p _site/recurse/dzf/{}

# task management
mkdir -p _site/recurse/tasks
mkdir -p _site/recurse/taskgroups

weewiki sync
weewiki export
rsync -rvt css/style.css _site/recurse/css
rsync -rvt css/code.css _site/recurse/css
