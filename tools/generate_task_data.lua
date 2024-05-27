descript = require("tools/descript")
pp = require("pprint")

function basename(str)
	local name = string.gsub(str, "(.*/)(.*)", "%2")
	return name
end

assert(#arg > 0, "supply a filename")

filename = arg[1]
fp = io.open(filename, "r")

data = descript.parse(fp:read("*all"))
fp:close()

task_group_descr = nil

local tasks_table = table.concat({
    "CREATE TABLE IF NOT EXISTS tasks(",
    "name TEXT UNIQUE, ",
    "title TEXT, ",
    "description TEXT, ",
    "task_group TEXT); ",
}, "\n")

local task_group_descriptions_table = table.concat({
    "CREATE TABLE IF NOT EXISTS task_group_descriptions(",
    "name TEXT UNIQUE, ",
    "description TEXT); ",
}, "\n")

group_name = basename(filename):gsub("[.]txt", "")

fmt = string.format

function escape_quotes(str)
    return str:gsub("'", "''")
end

print(task_group_descriptions_table)
print(tasks_table)

for _,blk in pairs(data) do
    if string.char(string.byte(blk[1], 1)) == "!" then
        if string.sub(blk[1], 1, 6) == "!desc " then
            local lines = {}
            table.insert(lines, string.sub(blk[1], 7))
            for i = 2, #blk do
                if blk[i] ~= "" then
                    table.insert(lines, blk[i])
                end
            end
            task_group_descr = table.concat(lines, " ")
        end

        print(fmt("INSERT INTO task_group_descriptions(name, description) "..
            "VALUES ('%s', '%s');", group_name, escape_quotes(task_group_descr)))
    else
        local first_space = blk[1]:find(" ")
        local task_name = blk[1]:sub(1, first_space - 1)
        local task_title = blk[1]:sub(first_space + 1)
        local task_blurb = {}
        for i=2,#blk do
            if (blk[i] ~= "") then
                table.insert(task_blurb, blk[i])
            end
        end

        task_blurb = table.concat(task_blurb, " ")

        print(fmt("INSERT INTO tasks(name, title, description, task_group) "..
            "VALUES ('%s', '%s', '%s', '%s');",
            task_name,
            escape_quotes(task_title),
            escape_quotes(task_blurb),
            group_name))
        -- print(task_blurb)
    end
end
