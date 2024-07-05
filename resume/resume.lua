db = sqlite3.open("resume.db")
json = dofile("../tools/json.lua")

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


function header1(str)
    return "# " .. str .. "\n"
end

function header2(str)
    return "## " .. str .. "\n"
end

function header3(str)
    return "### " .. str .. "\n"
end

function begin_list()
    return ""
end

function end_list()
    return "\n"
end

function item(str)
    return "- " .. str .. "\n"
end

function experience(fp)
    fp:write(header2("Experience"))
    local experience_name = "resume/experience"
    local nid = get_node_id(db, experience_name)
    assert(nid > 0,
        "Could not find node " .. experience_name)


    local explst = get_node_list(db, nid)

    for _, v in pairs(explst) do
        local title = get_node_lines(db, v)
        fp:write(header3(title))
        local points = get_node_list(db, v)

        if #points > 0 then
            fp:write(begin_list())
            for _, li in pairs(points) do
                fp:write(item(get_node_lines(db, li)))
            end
            fp:write(end_list())
        end
    end

end

function projects(fp)
    fp:write(header2("Projects"))
    local node_name = "resume/projects"
    local nid = get_node_id(db, node_name)
    assert(nid > 0,
        "Could not find node " .. node_name)


    local explst = get_node_list(db, nid)

    for _, v in pairs(explst) do
        local title = get_node_lines(db, v)
        fp:write(header3(title))
    end
end

function skills(fp)
    fp:write(header2("Skills"))
    local node_name = "resume/skills"
    local nid = get_node_id(db, node_name)
    assert(nid > 0,
        "Could not find node " .. node_name)


    local explst = get_node_list(db, nid)

    fp:write(begin_list())
    for _, v in pairs(explst) do
        local skillset = get_node_lines(db, v)
        fp:write(item(skillset))
    end
    fp:write(end_list())
end

function education(fp)
    fp:write(header2("Education"))

    local node_name = "resume/education"
    local nid = get_node_id(db, node_name)
    assert(nid > 0,
        "Could not find node " .. node_name)


    local explst = get_node_list(db, nid)

    fp:write(begin_list())
    for _, v in pairs(explst) do
        local skillset = get_node_lines(db, v)
        fp:write(item(skillset))
    end
    fp:write(end_list())
end

function generate(fp)
    fp:write(header1("Resume"))
    experience(md)
    projects(md)
    skills(md)
    education(md)
end

md = io.open("out.md", "w")

generate(md)

md:close()
