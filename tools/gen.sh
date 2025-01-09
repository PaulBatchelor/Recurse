# generate dagzet and wiki pages
./tools/gendb.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi

# generate logs
./tools/genlogdb.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi

./tools/dz_wikigen.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi

# generate tasks and wiki pages
./tools/gentasks.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi
./tools/generate_task_pages.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi
./tools/generate_taskgroup_pages.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi

# code study
./tools/import_codestudy.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi

# to be called after dagzet is created
./tools/gendzfiles.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi

# generate tag nodes

python3 tools/gentagnodes.py

# and then add their connections

dagzet knowledge/zzz_logs.dz | sqlite3 a.db
dagzet codestudy/zzz_logs.dz | sqlite3 a.db
