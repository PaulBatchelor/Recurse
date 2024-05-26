descript = require("tools/descript")
pp = require("pprint")

assert(#arg > 0, "supply a filename")

filename = arg[1]
fp = io.open(filename, "r")

data = descript.parse(fp:read("*all"))
fp:close()

task_group_descr = nil

for _,blk in pairs(data) do
    if string.char(string.byte(blk[1], 1)) == "!" then
        if string.sub(blk[1], 1, 6) == "!desc " then
            task_descr = string.sub(blk[1], 7)
        end
    else
        local first_space = blk[1]:find(" ")
        local task_name = blk[1]:sub(1, first_space)
        local task_desc = blk[1]:sub(first_space + 1)
        print(task_name, task_desc)
        local task_blurb = {}
        for i=2,#blk do
            if (blk[i] ~= "") then
                table.insert(task_blurb, blk[i])
            end
        end

        task_blurb = table.concat(task_blurb, " ")

        print(task_blurb)
    end
end

