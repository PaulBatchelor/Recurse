mkdir -p _site/recurse
mkdir -p _site/recurse/css
weewiki sync
weewiki export
rsync -rvt css/style.css _site/recurse/css
