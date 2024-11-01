mnolth lua tools/generate_graph_data.lua
if [ ! $? -eq 0 ]
then
    exit 1
fi
sqlite3 a.db < write_wiki_pages.sql
