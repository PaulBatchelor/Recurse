db = sqlite3.open("resume.db")
json = dofile("../tools/json.lua")
tex_backend = require("tex")

function get_node_id(db, name)
    local stmt = db:prepare(
        "SELECT id FROM dz_nodes " ..
        "WHERE name is '"  .. name .. "'"
    )

    local nid = -1

    for row in stmt:nrows() do
        nid = row.id
    end

    return nid
end

function get_node_name(db, nid)
    local stmt = db:prepare(
        "SELECT name FROM dz_nodes " ..
        "WHERE id == '"  .. nid .. "'"
    )

    local name = nil

    for row in stmt:nrows() do
        name = row.name
    end

    return name

end

function get_node_list(db, nid)
    local lst = {}

    local stmt = db:prepare(
        "SELECT item FROM dz_lists " ..
        "WHERE node == "  .. nid..
        " ORDER BY position"
    )


    local nid = -1

    for row in stmt:nrows() do
        table.insert(lst, row.item)
    end

    return lst

end

function get_node_lines(db, nid)
    local stmt = db:prepare(
        "SELECT lines FROM dz_lines " ..
        "WHERE node == '"  .. nid .. "'"
    )

    local lines_txt = ""

    for row in stmt:nrows() do
        lines_txt = row.lines
    end

    return table.concat(json.decode(lines_txt), " ")
end

markdown_backend = {
    prelude = function() end,

    epilogue = function() end,

    header1 = function (str)
        return "# " .. str .. "\n"
    end,

    header2 = function(str)
        return "## " .. str .. "\n"
    end,

    header3 = function (str)
        return "### " .. str .. "\n"
    end,

    begin_list = function ()
        return ""
    end,

    end_list = function()
        return "\n"
    end,

    item = function (str)
        return "- " .. str .. "\n"
    end
}


function experience(fp, backend)
    fp:write(backend.header2("Experience"))
    local experience_name = "resume/experience"
    local nid = get_node_id(db, experience_name)
    assert(nid > 0,
        "Could not find node " .. experience_name)


    local explst = get_node_list(db, nid)

    for _, v in pairs(explst) do
        local title = get_node_lines(db, v)
        fp:write(backend.header3(title))
        local points = get_node_list(db, v)

        if #points > 0 then
            fp:write(backend.begin_list())
            for _, li in pairs(points) do
                fp:write(backend.item(get_node_lines(db, li)))
            end
            fp:write(backend.end_list())
        end
    end

end

function projects(fp, backend)
    fp:write(backend.header2("Projects"))
    local node_name = "resume/projects"
    local nid = get_node_id(db, node_name)
    assert(nid > 0,
        "Could not find node " .. node_name)


    local explst = get_node_list(db, nid)

    for _, v in pairs(explst) do
        local title = get_node_lines(db, v)
        fp:write(backend.header3(title))
        local points = get_node_list(db, v)

        if #points > 0 then
            fp:write(backend.begin_list())
            for _, li in pairs(points) do
                fp:write(backend.item(get_node_lines(db, li)))
            end
            fp:write(backend.end_list())
        end
    end
end

function skills(fp, backend)
    fp:write(backend.header2("Skills"))
    local node_name = "resume/skills"
    local nid = get_node_id(db, node_name)
    assert(nid > 0,
        "Could not find node " .. node_name)


    local explst = get_node_list(db, nid)

    fp:write(backend.begin_list())
    for _, v in pairs(explst) do
        local skillset = get_node_lines(db, v)
        fp:write(backend.item(skillset))
    end
    fp:write(backend.end_list())
end

function education(fp, backend)
    fp:write(backend.header2("Education"))

    local node_name = "resume/education"
    local nid = get_node_id(db, node_name)
    assert(nid > 0,
        "Could not find node " .. node_name)


    local explst = get_node_list(db, nid)

    fp:write(backend.begin_list())
    for _, v in pairs(explst) do
        local skillset = get_node_lines(db, v)
        fp:write(backend.item(skillset))
    end
    fp:write(backend.end_list())
end

function generate(fp, backend)
    fp:write(backend.prelude())
    fp:write(backend.header1("Paul Batchelor"))
    experience(fp, backend)
    projects(fp, backend)
    skills(fp, backend)
    education(fp, backend)
    fp:write(backend.epilogue())
end

md = io.open("out.md", "w")
generate(md, markdown_backend)
md:close()

tex = io.open("out.tex", "w")
generate(tex, tex_backend)
tex:close()

