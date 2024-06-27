#!/usr/local/bin/mnolth lua
json = require("tools/json")

if #arg < 1 then
    error("Usage: dagzet file.dz")
end

filename = arg[1]

fp = io.open(filename)

aliases = {}
nodes = {}
xnodes = {}
nnodes = 0
curnode = nil
namespace = nil
text = {}
connections = {}
remarks = {}
connection_remarks = {}
last_connection = nil
hyperlinks = {}
tags = {}
graph_remarks = {}
flashcards = {}
file_ranges = {}
last_file = nil
images = {}
audio = {}
pages = {}
todo = {}

function split_at_spaces(inputstr)
    local t = {}
    for str in string.gmatch(inputstr, "([^ ]+)") do
        table.insert(t, str)
    end
    return t
end

function does_conection_exist(edges, left, right)
    for _, e in pairs(edges) do
        if e[1] == left and e[2] == right then
            return true
        end
    end

    return false
end

function is_alias(nodename)
    return string.match(nodename, "^@") ~= nil
end

function alias_resolve(alias_name)
    -- remove '@' prefix
    local alias_name = string.sub(alias_name, 2)

    assert(aliases[alias_name] ~= nil,
       "could not find alias '" ..
       alias_name .. "'")

    return aliases[alias_name]
end

linpos = 0
handler = {
    -- new node
    nn = function(args)
        local name = args:gsub("%s+", "")
        if namespace then
            name = namespace .. "/" .. name
        end
        assert(nodes[name] == nil, "node already exists: " .. name)
        nnodes = nnodes + 1
        nodes[name] = nnodes
        curnode = name
    end,

    -- set namespace
    ns = function(args)
        namespace = args:gsub("%s+", "")
    end,

    -- new textline
    ln = function(args)
        if text[curnode] == nil then
            text[curnode] = {}
        end
        table.insert(text[curnode], args)
    end,

    -- connection
    co = function (args)
        local conpair = split_at_spaces(args)
        assert(#conpair >= 2,
            "Not enough arguments: " .. args .. " line " .. linpos)
        local use_last_node_left = false
        local use_last_node_right = false

        local left = conpair[1]

        if left == "$" then
            use_last_node_left = true
            left = curnode
        end

        local right = conpair[2]

        if right == "$" then
            use_last_node_right = true
            right = curnode
        end


        if namespace then
            if use_last_node_left ~= true then
                left = namespace .. "/" .. left
            end
            if use_last_node_right ~= true then
                right = namespace .. "/" .. right
            end
        end

        if (does_conection_exist(connections, left, right)) then
            error("Connection already made: "
                .. left  .. " -> " .. right)
        end
        table.insert(connections, {left, right})
        last_connection = {left, right}
    end,

    zz = function (args)
        -- comment
    end,

    rm = function (args)
        -- remark
        if remarks[curnode] == nil then
            remarks[curnode] = {}
        end
        table.insert(remarks[curnode], args)
    end,

    cr = function(args)
        -- connection remark
        assert(last_connection ~= nil,
            "No previous connection to make remark about")
        local cr = connection_remarks
        local lc = last_connection

        -- comment remarks are 2d lookup tables
        -- values can have multiple remarks appended to them
        if cr[lc[1]] == nil then
            cr[lc[1]] = {}
        end
        if cr[lc[1]][lc[2]] == nil then
            cr[lc[1]][lc[2]] = {}
        end

        table.insert(cr[lc[1]][lc[2]], args)
    end,

    hl = function (args)
        -- hyperlink
        -- only one hyperlink per node
        hyperlinks[curnode] = args
    end,

    tg = function (args)
        if tags[curnode] == nil then
            tags[curnode] = {}
        end
        local tags_split = split_at_spaces(args)

        for _, t in pairs(tags_split) do
            table.insert(tags[curnode], t)
        end
    end,

    gr = function(args)
        -- graph remarks
        assert(namespace ~= nil,
            "No active graph namespace selected")

        grem = graph_remarks

        if grem[namespace] == nil then
            grem[namespace] = {}
        end

        table.insert(grem[namespace], args)
    end,

    ff  = function (args)
        -- flashcard front
        assert(curnode ~= nil, "No node selected")
        if flashcards[curnode] == nil then
            flashcards[curnode] = {}
        end

        if flashcards[curnode].front == nil then
            flashcards[curnode].front = {}
        end
        table.insert(flashcards[curnode].front, args)
    end,

    fb  = function (args)
        -- flashcard back
        assert(curnode ~= nil, "No node selected")
        if flashcards[curnode] == nil then
            flashcards[curnode] = {}
        end

        if flashcards[curnode].back == nil then
            flashcards[curnode].back = {}
        end
        table.insert(flashcards[curnode].back, args)
    end,

    td = function(args)
        -- make TODO item
        assert(curnode ~= nil, "No node selected")

        if todo[curnode] == nil then
            todo[curnode] = {}
        end

        table.insert(todo[curnode], args)
    end,

    fr = function (args)
        -- file range (for code annotation)
        local tags_split = split_at_spaces(args)
        local filename = tags_split[1]
        local start_line = tags_split[2]
        local end_line = tags_split[3]

        if filename == "$" then
            assert(last_file ~= nil, "previous filename not set")
            filename = last_file
        end

        if end_line == nil then
            end_line = -1
        end

        file_ranges[curnode] = {filename, start_line, end_line}

        last_file = filename
    end,

    -- external connection (beyond namespace)
    cx = function (args)
        local conpair = split_at_spaces(args)
        assert(#conpair >= 2,
            "Not enough arguments: " .. args .. " line " .. linpos)

        -- TODO: deduplicate left/right logic

        local left = conpair[1]

        if is_alias(left) then
            left = alias_resolve(left)
        end

        if left == "$" then
            left = curnode
        else
            -- assumed external node, keep track of it
            if xnodes[left] == nil then
                xnodes[left] = true
            end
        end

        local right = conpair[2]
        if is_alias(right) then
            right = alias_resolve(right)
        end

        if right == "$" then
            right = curnode
        else
            -- assumed external node, keep track of it
            if xnodes[right] == nil then
                xnodes[right] = true
            end
        end

        if (does_conection_exist(connections, left, right)) then
            error("Connection already made: "
                .. left  .. " -> " .. right)
        end
        table.insert(connections, {left, right})
        last_connection = {left, right}
    end,

    -- node aliases (used in external connections)
    al = function(args)
        local args = split_at_spaces(args)
        assert(#args >= 2, "not enough arguments")
        local alias_name = args[1]
        local full_path = args[2]

        assert(aliases[alias_name] == nil,
            "alias '" .. alias_name .. "' already exists")

        aliases[alias_name] = full_path
    end,

    -- image
    im = function(args)
        images[curnode] = args
    end,

    -- equation
    eq = function(args)
        -- TODO: implement
    end,

    -- audio
    au = function(args)
        audio[curnode] = args
    end,

    -- pages
    pg = function(args)
        pages[curnode] = args
    end,
}

for ln in fp:lines() do
    linpos = linpos + 1
    if #ln >= 2 then
        local cmd = string.sub(ln, 1, 2)
        local args = string.sub(ln, 4)
        f = handler[cmd]
        if f ~= nil then
            f(args)
        else
            error("invalid command:" .. cmd)
        end
    end
end

function has_incoming_nodes(node, edges)
    for _, e in pairs(edges) do
        if e[2] == node then return true end
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

function does_loop_exist(edges, n, m)
    for _, e in pairs(edges) do
        if e[1] == m and e[2] == n then
            return true
        end
    end

    return false
end

function check_cycles()
    -- for k,v in pairs(nodes) do print(k,v) end
    local no_incoming = {}
    local sorted = {}

    local edges = {}

    for _, v in pairs(connections) do
        -- print(nodes[v[1]] .. " -> " .. nodes[v[2]])
        table.insert(edges, v)
    end

    for n, _ in pairs(nodes) do
        if has_incoming_nodes(n, edges) == false then
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

    local remaining_edges = 0

    for k, v in pairs(edges) do
        -- print(k, v)
        remaining_edges = remaining_edges + 1
    end

    if (remaining_edges > 0) then
        local found_loops = {}
        for _, v in pairs(edges) do
            -- print(v[1] .. " -> " .. v[2])
            if does_loop_exist(edges, v[1], v[2]) then
                table.insert(found_loops, v)
            end
        end

        if #found_loops > 0 then
            print("cycles found:")
            for _, loop in pairs(found_loops) do
                print(loop[1] .. " -> " .. loop[2])
            end
            error("Graph is cyclic. Remove the loops above.")
        end
    end

    -- for _,v in pairs(no_incoming) do
    --     print(nodes[v], v)
    -- end

end

function check_unknown_nodes()
    for _, v in pairs(connections) do
        if nodes[v[1]] == nil and xnodes[v[1]] == nil then
            error("Unknown node: " .. v[1])
        end
        if nodes[v[2]] == nil and xnodes[v[2]] == nil then
            error("Unknown node: " .. v[2])
        end
    end
end

function mkvarname(nodename)
    return nodename:gsub("/+", "_")
end

function print_dot()
    print ("digraph G {")
    print ("rankdir = \"BT\"")
    -- print ("rank = \"max\"")

    for _,v in pairs(connections) do
        local left = mkvarname(v[1])
        local right = mkvarname(v[2])
        print(left .. " -> " .. right)
    end

    for k,_ in pairs(nodes) do
        local name = mkvarname(k)
        if text[k] ~= nil then
            print(name .. "[label = \"" ..
                table.concat(text[k], " ") ..
                "\"]")
        end
    end

    print("}")
end

function name_lookup(name)
    return "(SELECT id FROM dz_nodes WHERE name IS '" ..
    name ..
    "' LIMIT 1)"
end

function generate_sqlite_code()
    local concat = table.concat
    local nodes_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_nodes(",
        "name TEXT UNIQUE,",
        "id INTEGER PRIMARY KEY,",
        "position INTEGER);"
    }, "\n")

    local connections_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_connections(",
        "left INTEGER,",
        "right INTEGER);",
    }, "\n")

    local lines_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_lines(",
        "node INTEGER,",
        "lines TEXT);",
    }, "\n")

    local remarks_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_remarks(",
        "node INTEGER,",
        "remarks TEXT);",
    }, "\n")

    local connection_remarks_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_connection_remarks(",
        "left INTEGER,",
        "right INTEGER,",
        "remarks TEXT);",
    }, "\n")

    local hyperlinks_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_hyperlinks(",
        "node INTEGER,",
        "hyperlink TEXT);",
    }, "\n")

    local tags_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_tags(",
        "node INTEGER,",
        "tag TEXT);",
    }, "\n")

    local graph_remarks_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_graph_remarks(",
        "namespace TEXT,",
        "remarks TEXT);",
    }, "\n")

    local flashcards_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_flashcards(",
        "node INTEGER,",
        "front TEXT,",
        "back TEXT);",
    }, "\n")

    local file_ranges_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_file_ranges(",
        "node INTEGER,",
        "filename TEXT,",
        "start INTEGER,",
        "end INTEGER);",
    }, "\n")

    local images_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_images(",
        "node INTEGER,",
        "image TEXT);",
    }, "\n")

    local audio_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_audio(",
        "node INTEGER,",
        "audio TEXT);",
    }, "\n")

    local pages_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_pages(",
        "node INTEGER,",
        "page INTEGER);",
    }, "\n")

    local todo_table = concat({
        "CREATE TABLE IF NOT EXISTS dz_todo(",
        "node INTEGER,",
        "task STRING);",
    }, "\n")

    print("BEGIN;");
    print(nodes_table)
    print(connections_table)
    print(lines_table)
    print(remarks_table)
    print(connection_remarks_table)
    print(hyperlinks_table)
    print(tags_table)
    print(graph_remarks_table)
    print(flashcards_table)
    print(file_ranges_table)
    print(images_table)
    print(audio_table)
    print(pages_table)
    print(todo_table)

    local fmt = string.format
    local nodelist = {}

    for k, _ in pairs(nodes) do
        table.insert(nodelist, k)
    end

    table.sort(nodelist)

    for _, v in pairs(nodelist) do
        print(fmt("INSERT INTO dz_nodes(name, position) " ..
            "VALUES (\'%s\', %d);", v, nodes[v]))
    end
    print("COMMIT;");

    print("BEGIN;")
    for _, v in pairs(connections) do
        local left_id = name_lookup(v[1])
        local right_id = name_lookup(v[2])
        print(fmt("INSERT INTO dz_connections(left, right) "..
            "VALUES (%s, %s);", left_id, right_id))
    end

    for k, v in pairs(text) do
        print(fmt("INSERT INTO dz_lines(node, lines) "..
            "VALUES (%s, '%s');",
            name_lookup(k),
            json.encode(v):gsub("'", "''")))
    end

    for k, v in pairs(remarks) do
        print(fmt("INSERT INTO dz_remarks(node, remarks) "..
            "VALUES (%s, '%s');",
            name_lookup(k),
            json.encode(v):gsub("'", "''")))
    end

    for left, v in pairs(connection_remarks) do
        for right, rmk in pairs(v) do
            print(fmt("INSERT INTO " ..
                "dz_connection_remarks(left, right, remarks) "..
                "VALUES (%s, %s, '%s');",
                name_lookup(left), name_lookup(right),
                json.encode(rmk):gsub("'", "''")))
        end
    end

    for k, v in pairs(hyperlinks) do
        print(fmt("INSERT INTO dz_hyperlinks(node, hyperlink) "..
            "VALUES (%s, '%s');",
            name_lookup(k),
            v))
    end

    for k, v in pairs(tags) do
        -- insert tags individually. This should make
        -- sqlite queries a bit easier
        for _, t in pairs(v) do
            print(fmt("INSERT INTO dz_tags(node, tag) "..
                "VALUES (%s, '%s');",
                name_lookup(k),
                t))
        end
    end

    for ns, rmk in pairs(graph_remarks) do
        print(fmt("INSERT INTO dz_graph_remarks(namespace, remarks) "..
            "VALUES (%s, '%s');",
            "'" .. ns .. "'",
            json.encode(rmk):gsub("'", "''")))
    end

    for k, v in pairs(flashcards) do
        print(fmt("INSERT INTO dz_flashcards(node, front, back) "..
            "VALUES (%s, '%s', '%s');",
            name_lookup(k),
            json.encode(v.front or {}):gsub("'", "''"),
            json.encode(v.back or {}):gsub("'", "''")))
    end

    for k,v in pairs(file_ranges) do
        print(fmt("INSERT INTO dz_file_ranges(node, filename, start, end) "..
            "VALUES (%s, '%s', %d, %d);",
            name_lookup(k),
            v[1],
            v[2],
            v[3]))
    end

    for k,v in pairs(images) do
        print(fmt("INSERT INTO dz_images(node, image) "..
            "VALUES (%s, '%s');",
            name_lookup(k),
            v))
    end

    for k,v in pairs(audio) do
        print(fmt("INSERT INTO dz_audio(node, audio) "..
            "VALUES (%s, '%s');",
            name_lookup(k),
            v))
    end

    for k,v in pairs(pages) do
        print(fmt("INSERT INTO dz_pages(node, page) "..
            "VALUES (%s, %s);",
            name_lookup(k),
            v))
    end

    for k,v in pairs(todo) do
        print(fmt("INSERT INTO dz_todo(node, task) "..
            "VALUES (%s, '%s');",
            name_lookup(k),
            table.concat(v, " ")))
    end

    print("COMMIT;");
end

check_cycles()
check_unknown_nodes()
generate_sqlite_code()
-- print_dot()
