sqlite3 a.db <<EOF
    DROP TABLE IF EXISTS tasks;
    DROP TABLE IF EXISTS task_group_descriptions;
EOF

while read -r line
do
    echo $line
    mnolth lua tools/generate_task_data.lua $line | sqlite3 a.db
    if [ ! $? -eq 0 ]
    then
        exit
    fi
done < tasks/taskfiles.txt
