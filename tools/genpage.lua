genpage = {}

function generate_nodes(db, namespace)
    local stmt = db:prepare(
        "SELECT name, id FROM dz_nodes " ..
        "WHERE name LIKE '" .. namespace .. "/%'" ..
        "ORDER by name ASC;"
    )

    assert(stmt, "Could not prepare statement")

    local nodes = {}

    for row in stmt:nrows() do
        nodes[row.id] = row.name
    end
    stmt:finalize()
    return nodes
end

function insert_connections_from_stmt(connections, stmt, nodes)
    for row in stmt:nrows() do
        if connections[row.left] == nil then
            connections[row.left] = {}
        end
        if row.right == nil  then
            stmt:finalize()
            assert(nodes ~= nil, "nodes table does not exist. is it being passed in?")
            error("could not find from left connection: " .. nodes[row.left])
        end
        connections[row.left][row.right] = true
    end
end

function insert_connections(connections, db, id, nodes)
    local stmt = db:prepare(
        "SELECT left, right FROM dz_connections " ..
        "WHERE left == ".. id .. ";"
    )
    assert(stmt, "Could not prepare statement")
    insert_connections_from_stmt(connections, stmt, nodes)
    stmt:finalize()

    local stmt = db:prepare(
        "SELECT left, right FROM dz_connections " ..
        "WHERE right == ".. id .. ";"
    )
    assert(stmt, "Could not prepare statement")
    insert_connections_from_stmt(connections, stmt, nodes)
    stmt:finalize()
end

function create_connections(db, nodes)
    local connections = {}
    for id,_ in pairs(nodes) do
        insert_connections(connections, db, id, nodes)
    end

    return connections
end

function has_incoming_nodes(node, edges, nodelist)
    for _, e in pairs(edges) do
        if nodelist ~= nil then
            -- the receiving node of an incoming node must
            -- local to the subgraph
            if nodelist[e[1]] ~= nil and e[2] == node then return true end
        else
            if e[2] == node then return true end
        end
    end

    return false
end

-- find all nodes m where n -> m
function nodes_connected_to(node, edges)
    local nodelist = {}

    for _, e in pairs(edges) do
        if e[1] == node then
            table.insert(nodelist, e[2])
        end
    end

    return nodelist
end

function remove_edge(edges, n, m)
    for idx, e in pairs(edges) do
        if e[1] == n and e[2] == m then
            edges[idx] = nil
        end
    end
end

function topsort(nodes, connections)
    local no_incoming = {}
    local sorted = {}

    local edges = {}
    local xnodes = {}

    for left, rcons in pairs(connections) do
        -- print(nodes[v[1]] .. " -> " .. nodes[v[2]])
        for right, _ in pairs(rcons) do
            table.insert(edges, {left, right})
        end
    end

    for n, _ in pairs(nodes) do
        if has_incoming_nodes(n, edges, nodes) == false then
            table.insert(no_incoming, n)
        end
    end

    while #no_incoming > 0 do
        local n = table.remove(no_incoming)
        local nodesfrom = nodes_connected_to(n, edges)
        table.insert(sorted, n)
        for _,m in pairs(nodesfrom) do
            remove_edge(edges, n, m)
            if has_incoming_nodes(m, edges) == false then
                table.insert(no_incoming, m)
            end
        end
    end

    return sorted
end

function get_children(connections, nid)
    local children = {}
    for left, rcons  in pairs(connections) do
        for right, _ in pairs(rcons) do
            if right == nid then
                table.insert(children, left)
            end
        end
    end

    return children
end

function get_parents(connections, nid)
    local parents = {}

    if connections[nid] ~= nil then
        for right, _ in pairs(connections[nid]) do
            table.insert(parents, right)
        end
    end

    return parents
end

function shortname(namespace, name)
    local newstr = name:gsub(namespace .. "/", "")
    return newstr
end

function get_lines(db, nid)
    local stmt = db:prepare(
        "SELECT lines FROM dz_lines " ..
        "WHERE node == " .. nid ..
        " LIMIT 1;"
    )

    local lines = nil
    for row in stmt:nrows() do
        lines = row.lines
    end

    if lines ~= nil then
        lines = json.decode(lines)
    end
    stmt:finalize()
    return lines
end

function get_remarks(db, nid)
    local stmt = db:prepare(
        "SELECT remarks FROM dz_remarks " ..
        "WHERE node == " .. nid ..
        " LIMIT 1;"
    )

    local remarks = nil
    for row in stmt:nrows() do
        remarks = row.remarks
    end

    if remarks ~= nil then
        remarks = json.decode(remarks)
    end
    stmt:finalize()
    return remarks
end

function get_hyperlink(db, nid)
    local stmt = db:prepare(
        "SELECT hyperlink FROM dz_hyperlinks " ..
        "WHERE node == " .. nid ..
        " LIMIT 1;"
    )

    local hyperlink = nil
    for row in stmt:nrows() do
        hyperlink = row.hyperlink
    end

    stmt:finalize()
    return hyperlink
end

function get_tags(db, nid)
    local stmt = db:prepare(
        "SELECT tag FROM dz_tags " ..
        "WHERE node == " .. nid ..
        ";"
    )

    local tags = nil
    for row in stmt:nrows() do
        if tags == nil then
            tags = {}
        end
        table.insert(tags, row.tag)
    end

    stmt:finalize()
    return tags
end

function get_connection_remarks(db, left, right)
    local stmt = db:prepare(
        "SELECT remarks FROM dz_connection_remarks " ..
        "WHERE left == " .. left ..
        " AND right == " .. right ..
        " LIMIT 1;"
    )

    local remarks = nil
    for row in stmt:nrows() do
        remarks = row.remarks
    end

    if remarks ~= nil then
        remarks = json.decode(remarks)
    end
    stmt:finalize()
    return remarks
end

function get_flashcard(db, nid)
    local stmt = db:prepare(
        "SELECT front, back FROM dz_flashcards " ..
        "WHERE node == " .. nid ..
        " LIMIT 1;"
    )

    local card = nil
    for row in stmt:nrows() do
        card = {}
        card.front = row.front
        card.back = row.back
    end

    if card ~= nil then
        card.front = json.decode(card.front)
        card.back = json.decode(card.back)
    end

    stmt:finalize()
    return card
end

function get_image(db, nid)
    local stmt = db:prepare(
        "SELECT image FROM dz_images " ..
        "WHERE node == " .. nid ..
        " LIMIT 1;"
    )

    local img = nil
    for row in stmt:nrows() do
        img = row.image
    end

    stmt:finalize()
    return img 
end

function get_audio(db, nid)
    local stmt = db:prepare(
        "SELECT audio FROM dz_audio " ..
        "WHERE node == " .. nid ..
        " LIMIT 1;"
    )

    local audio = nil
    for row in stmt:nrows() do
        audio = row.audio
    end

    stmt:finalize()
    return audio 
end

function lookup_name_from_id(db, id)
    local stmt = db:prepare(
        "SELECT name FROM dz_nodes " ..
        "WHERE id == ".. id .. " LIMIT 1;"
    )

    local name = nil
    for row in stmt:nrows() do
        name = row.name
    end

    stmt:finalize()

    return name
end

function get_position(db, nid)
    local stmt = db:prepare(
        "SELECT position FROM dz_nodes " ..
        "WHERE id == " .. nid ..
        " LIMIT 1;"
    )

    local pos = nil
    for row in stmt:nrows() do
        pos = row.position
    end

    stmt:finalize()
    return pos
end


function generate_node_data(nodes, connections, namespace, db, nid)
    local children = get_children(connections, nid)
    local parents = get_parents(connections, nid)
    local lines = get_lines(db, nid)
    local remarks = get_remarks(db, nid)
    local hyperlink = get_hyperlink(db, nid)
    local tags = get_tags(db, nid)
    local card = get_flashcard(db, nid)
    local img = get_image(db, nid)
    local pos = get_position(db, nid)
    local audio = get_audio(db, nid)

    local ns = namespace
    local node = {}
    node.parents = {}
    node.children = {}
    for _, p in pairs(parents) do
        local val = nil
        if nodes[p] == nil then
            val = lookup_name_from_id(db, p)
        else
            val = shortname(ns, nodes[p])
        end
        -- not sure seeing connection remarks from child->parent
        -- makes much sense, since usually the relationship
        -- describes what the child (small topic) is doing
        -- relative to the parent (large topic)
        -- local cr = get_connection_remarks(db, nid, p)
        -- if cr ~= nil then
        --     local newval = {}
        --     newval.name = val
        --     newval.remarks = cr
        --     val = newval
        -- end
        table.insert(node.parents, val)
    end

    for _, c in pairs(children) do
        local nodename = nil
        local val = nil
        -- TODO: deduplicate this logic
        if nodes[c] == nil then
            nodename = lookup_name_from_id(db, c)
        else
            nodename = shortname(ns, nodes[c])
        end

        val = nodename

        local cr = get_connection_remarks(db, c, nid)
        if cr ~= nil then
            local newval = {}
            newval.name = val
            newval.remarks = cr
            val = newval
        end

        table.insert(node.children, val)
    end

    if nodes[nid] == nil then

        node.name = lookup_name_from_id(db, nid)
        assert(node.name ~= nil,
            "could not find node with id " .. nid)
    else
        node.name = shortname(ns, nodes[nid])
    end

    node.lines = lines
    node.remarks = remarks
    node.hyperlink = hyperlink
    node.tags = tags
    node.flashcard = card
    node.image = img
    node.position = pos
    node.nid = nid
    node.audio = audio

    return node, children
end

function traverse_node(params, nid)
    if params.traversed[nid] == nil then
        local node, children  =
            generate_node_data(params.nodes,
                               params.connections,
                               params.namespace,
                               params.db,
                               nid)
        table.insert(params.nodelist, node)
        params.traversed[nid] = true
        return children
    end
    return {}
end

function traverse_children(params, children_nids)
    local next_children_nids = {}
    for _, c in pairs(children_nids) do
        local tmp = traverse_node(params, c)
        for _,v in pairs(tmp) do
            table.insert(next_children_nids, v)
        end
    end
    return next_children_nids
end

function any_local_nodes(receiving_nodes, local_nodelist)
    for nid, _ in pairs(receiving_nodes) do
        if local_nodelist[nid] ~= nil then return true end
    end

    return false
end

function get_top_nodes(nodes, connections)
    local top_nodes = {}
    for nid, _ in pairs(nodes) do

        -- edge case: local nodes that are only children
        -- to external nodes will not show up as
        -- a top-level node to this graph without special
        -- checking for local nodes in the receiving
        -- connections
        if
            connections[nid] == nil or
            any_local_nodes(connections[nid], nodes) == false
        then
            table.insert(top_nodes, nid)
        end
    end
    return top_nodes
end

function append_tree(tree, nodes, connections, namespace, nid, db, xnodes)
    local newtree = childtree(nodes, connections, namespace, nid, db, xnodes)
    table.insert(tree, newtree)
end

function childtree(nodes, connections, namespace, nid, db, xnodes)
    local tree = {}
    local tree_nodes = {}

    assert(db ~= nil, "must SQLite provide database")
    -- TODO figure out way to find external nodes before
    -- this point. Create xnodes table.
    -- assert(nodes[nid] ~= nil, "could not find node with id: " .. nid)

    local external_node = false
    local node_name = nil
    if nodes[nid] == nil then
        -- possibly an external node outside of current namespace,
        -- look up name from node id
        local xnode_name = lookup_name_from_id(db, nid)
        assert(xnode_name ~= nil,
            "Could not find node with id " .. nid)
        xnodes[xnode_name] = nid
        external_node = true
        node_name = xnode_name
        -- print(nid, xnode_name)
    end

    if external_node == false then
        node_name = shortname(namespace, nodes[nid])
    end

    local children = get_children(connections, nid)

    -- list structure: (name (child1 child2 ... childN))
    table.insert(tree, node_name)
    for _,c in pairs(children) do
        append_tree(tree_nodes, nodes, connections, namespace, c, db, xnodes)
    end

    -- tree node has no children, just return a string
    if #tree_nodes == 0 then
        tree = tree[1]
    else
        table.insert(tree, tree_nodes)
    end

    return tree
end

function generate_tree(nodes, connections, namespace, db)
    local top_nodes = get_top_nodes(nodes, connections)
    local tree = {}
    local xnodes = {}
    for _, top in pairs(top_nodes) do
        append_tree(tree, nodes, connections, namespace, top, db, xnodes)
    end

    return tree, xnodes
end

function get_graph_remarks(db, namespace)
    local stmt = db:prepare(
        "SELECT remarks FROM dz_graph_remarks " ..
        "WHERE namespace is '" .. namespace .. "';"
    )

    local remarks = nil
    for row in stmt:nrows() do
        remarks = row.remarks
    end

    if remarks ~= nil then
        remarks = json.decode(remarks)
    end
    stmt:finalize()
    return remarks
end

function genpage.pagedata(db, namespace, nodes)
    -- local nodes = generate_nodes(db, namespace)
    local connections = create_connections(db, nodes)
    local output = {}

    -- dynamically populated from traversal
    local nodelist = {}

    -- keeps track of nodes that have been traversed already
    local traversed = {}

    -- TODO topological sort doesn't end up including all
    -- local nodes
    local sorted = topsort(nodes, connections)

    -- shove stuff into a table
    local params = {
        nodes = nodes,
        connections = connections,
        namespace = namespace,
        db = db,
        traversed = traversed,
        nodelist = nodelist
    }

    for i=#sorted,1, -1 do
        local nid = sorted[i]

        if traversed[nid] == nil then
            local children_nids = traverse_node(params, sorted[i])

            while #children_nids > 0 do
                children_nids = traverse_children(params, children_nids)
            end
        end
    end

    output.nodes = params.nodelist
    output.namespace = namespace
    tree, xnodes =
        generate_tree(nodes, connections, namespace, db)
    output.tree = tree
    output.xnodes = xnodes
    output.remarks = get_graph_remarks(db, namespace)

    return output
end

return genpage
