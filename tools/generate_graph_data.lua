json = require("tools/json")
pprint = require("tools/pprint")
genpage = require("tools/genpage")
function split_at_slashes(inputstr)
    local t = {}
    for str in string.gmatch(inputstr, "([^/]+)") do
        table.insert(t, str)
    end
    return t
end

function create_hierarchy(db)
    local h = {}
    local lookup = {}
    local positions = {}
    local stmt = db:prepare(
        "SELECT name, id, position FROM dz_nodes " ..
        "ORDER by name ASC;"
    )

    for row in stmt:nrows() do
        local names = split_at_slashes(row.name)
        local top = h
        for _,nm in pairs(names) do
            if top[nm] == nil then
                top[nm] = {}
            end
            top = top[nm]
        end
        lookup[row.name] = row.id
        -- TODO not being used?
        positions[row.name] = row.position
    end

    return h, lookup
end

function cdr(levels, name)
    local s = {}

    for _,v in pairs(levels) do
        table.insert(s, v)
    end
    table.insert(s, name)
    return s
end

function tree_size(h)
    local sz = 0
    for _,_ in pairs(h) do
        sz = sz + 1
    end

    return sz
end


function generate_page_data(db, h, lookup, namespace, pglist, data_files)
    local nodes = {}
    local subgraphs = {}
    namespace = namespace or {}
    pglist = pglist or {}
    for name, children in pairs(h) do
        local nchildren = tree_size(children)
        if nchildren > 0 then
            table.insert(subgraphs, name)
            table.insert(namespace, name)
            generate_page_data(db, children, lookup, namespace, pglist, data_files)

            -- subgraph may sometimes be a node
            local fullpath = name
            if #namespace > 0 then
                fullpath =
                    table.concat(namespace, "/")
            end
            local nid = lookup[fullpath]

            if nid ~= nil then
                nodes[nid] = fullpath
            end

            table.remove(namespace)
        else
            local fullpath = name
            if #namespace > 0 then
                fullpath =
                    table.concat(namespace, "/") .. "/" .. name
            end
            local nid = lookup[fullpath]
            assert(nid ~= nil, "could not find: " .. fullpath)
            nodes[nid] = fullpath
        end
    end


    local nspath = table.concat(namespace, "/")
    local filepath = "data"

    -- top path "data/index.json" should have only 1 "/"
    if #namespace > 0 then
        filepath = filepath .. "/"
    end

    table.insert(pglist, nspath)
    filepath = filepath .. nspath .. "/index.json"

    local output = genpage.pagedata(db, nspath, nodes)
    output.subgraphs = subgraphs

    local encoded_data = json.encode(output)
    print("writing to " .. filepath)
    -- local fp = io.open(filepath, "w")
    -- fp:write(encoded_data)
    -- fp:close()

    data_files.keys:write(
        "/" .. nspath ..
        ":" ..
        data_files.offset ..
        ":" ..
        encoded_data:len() ..
        "\n")

    data_files.contents:write(encoded_data)

    data_files.offset = data_files.offset + encoded_data:len()


    return pglist
end

function generate_data_files()
    local data = {}
    data.offset = 0
    data.keys = io.open("data_keys", "w")
    data.contents = io.open("data_contents", "w")
    return data
end

db = sqlite3.open("a.db")

local h, lookup, positions = create_hierarchy(db)

data_files = generate_data_files()
pglist = generate_page_data(db, h, lookup, nil, nil, data_files)
data_files.keys:close()
data_files.contents:close()

sql = {}
table.insert(sql, "DELETE FROM wiki WHERE key like 'dz/%';")
table.insert(sql, "DELETE FROM wiki WHERE key is 'dz';")
table.insert(sql, "BEGIN;")
table.insert(sql, "INSERT INTO wiki(key, value) VALUES")

function dzcmdstr(path)
    return "@!(dagzet-page \"" .. path .. "\")!@"
end

wiki_pages = {}
for _, pg in pairs(pglist) do
    -- if pg == "" then
    --     table.insert(wiki_pages,
    --         "('dz', '".. dzcmdstr("data/index.json") .."')")
    -- else
    --     table.insert(wiki_pages,
    --         string.format("(%s, %s)",
    --             "'dz/" .. pg .. "'",
    --             "'" ..
    --                 dzcmdstr("data/" .. 
    --                     pg .. "/index.json")
    --                 ..
    --             "'"
    --                 ))
    -- end
    if pg == "" then
        table.insert(wiki_pages,
            "('dz', '".. dzcmdstr("/") .."')")
    else
        table.insert(wiki_pages,
            string.format("(%s, %s)",
                "'dz/" .. pg .. "'",
                "'" ..
                    dzcmdstr("/" ..  pg)
                    ..
                "'"
                    ))
    end
end
table.insert(sql, table.concat(wiki_pages, ",\n"))
table.insert(sql, ";")
table.insert(sql, "COMMIT;")

sql_outfile = "write_wiki_pages.sql"

fp = io.open(sql_outfile, "w")
fp:write(table.concat(sql, "\n"))
fp:close()
print("Wrote weewiki SQL insert statements to " .. sql_outfile)
