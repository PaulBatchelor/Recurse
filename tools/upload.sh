rm -r _live/recurse
rsync -rvt _site/recurse/* _live/recurse

# git add recurse;
# git commit -m "recurse updates";
# git push origin master
# ssh paul@pbat.ch "cd paulbatchelor.github.io; git pull"
