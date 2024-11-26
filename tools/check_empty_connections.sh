echo -e "Empty left connections:\n"
sqlite3 a.db <<EOM
    SELECT dz_nodes.name
    FROM dz_connections
    INNER JOIN dz_nodes on dz_connections.right = dz_nodes.id
    WHERE left is NULL
EOM

# echo -e "\nEmpty right connections:\n"
# sqlite3 a.db <<EOM
#     SELECT dz_nodes.name
#     FROM dz_connections
#     INNER JOIN dz_nodes on dz_connections.left = dz_nodes.id
#     WHERE right is NULL
# EOM
