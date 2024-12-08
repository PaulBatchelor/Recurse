descript = require("tools/descript")

assert(#arg > 0, "supply a filename")

filename = arg[1]
fp = io.open(filename, "r")

data = descript.parse(fp:read("*all"))
fp:close()

num = lpeg.R("09")
year = lpeg.Cg(num*num*num*num, "year")
month = lpeg.Cg(num*num, "month")
day = lpeg.Cg(num*num, "day")
local t = lpeg.locale()
category = (lpeg.P("#") * t.alnum^1)^0
category = lpeg.Cg(category, "category")
dash = "-"
comment = lpeg.P(" ")^0 * lpeg.Cg(lpeg.Cp(), "comment_start")

date = lpeg.Ct(year * dash * month * dash * day * category * comment)
-- date = lpeg.Ct(year * dash * month * dash * day * comment)

hours = lpeg.Cg(num*num, "hours")
minutes = lpeg.Cg(num*num, "minutes")
colon = lpeg.P(":")

clocktime = lpeg.Ct(hours * colon * minutes * comment)

events = {}

day = nil

function is_date(str)
    local t = lpeg.match(date * comment, str)
    if t then
        return {
            date =
               string.format("%04d-%02d-%02d",
               t.year, t.month, t.day),
            title = string.sub(str, t.comment_start),
            category = string.sub(t.category, 2) or nil
        }
    end

    return nil
end

function is_time(str)
    local t = lpeg.match(clocktime * comment, str)
    if t then
        return {
            time =
               string.format("%02d:%02d",
               t.hours, t.minutes),
            title = string.sub(str, t.comment_start)
        }
    end

    return nil
end

function extract_comment (blk)
    local comment = nil
    for k,v in pairs(blk) do
        if k > 1 then
            if comment == nil then
                comment = {}
            end

            table.insert(comment, blk[k])
        end
    end
    return comment
end

for _,blk in pairs(data) do
   local obj = is_date(blk[1])
   if obj ~= nil then
        day = obj.date
        assert(events[day] == nil, "day " .. day .. " already exists")
        events[day] = {}
        events[day].title = obj.title
        events[day].comment = extract_comment(blk)
        events[day].events = {}
        events[day].category = obj.category
    else
        local obj = is_time(blk[1])
        assert(obj ~= nil, "invalid entry: " .. blk[1])
        if obj ~= nil then
            assert(events[day] ~= nil)
            local evt = {}
            evt.time = obj.time
            evt.title = obj.title
            evt.comment = extract_comment(blk)
            table.insert(events[day].events, evt)
        end
    end
end

local logs_table = table.concat({
    "CREATE TABLE IF NOT EXISTS logs(",
    "day TEXT, ",
    "time TEXT, ",
    "title TEXT, ",
    "comment TEXT, ",
    "position INTEGER, ",
    "category TEXT);",
}, "\n")

local dayblurbs_table = table.concat({
    "CREATE TABLE IF NOT EXISTS dayblurbs(",
    "day TEXT, ",
    "title TEXT, ",
    "blurb TEXT); ",
}, "\n")

local logtags_table = table.concat({
    "CREATE TABLE IF NOT EXISTS logtags(",
    "logid INTEGER, ",
    "tag TEXT); ",
}, "\n")

print(logs_table)
print(dayblurbs_table)
print(logtags_table)

fmt = string.format

function concat_comment(comment)
    if comment then
        local lines = {}
        local preformat = false
        local preblock = {}
        for _, line in pairs(comment) do
            -- if line == "---" then line = "\n" end

            if line == "===" then
                line = ""
                if preformat then
                    preformat = false
                    line = table.concat(preblock, "\n")
                    preblock = {}
                else
                    preformat = true
                end
            end

            if preformat then
                table.insert(preblock, line)
                line = ""
            end

            if line ~= "" then
                table.insert(lines, line)
            end
        end
        return table.concat(lines, " "):gsub("'", "''")
    end

    return ""
end

function extract_tags(title)
    for w in title:gmatch("%S+") do
        if (w:byte(1) == string.byte("#")) then
            local tag = w:sub(2)
            print(fmt("INSERT INTO logtags(logid, tag) " ..
                "VALUES (%s, '%s');",
                -- last inserted log entry
                "(SELECT max(rowid) from logs)",
                tag
                ))
        end
    end
end

print("BEGIN;")
for d,e in pairs(events) do
    if(e.comment or e.title) then
        print(fmt("INSERT INTO dayblurbs(day, title, blurb) "..
            "VALUES ('%s', '%s', '%s');",
            d, e.title or "", concat_comment(e.comment)))
    end

    for pos,evt in pairs(e.events) do
        print(fmt("INSERT INTO logs(day, time, title, comment, position, category) "..
            "VALUES ('%s', '%s', '%s', '%s', %d, '%s');",
            d, evt.time, evt.title:gsub("'", "''"), concat_comment(evt.comment), pos, e.category))
        extract_tags(evt.title)
    end
end
print("COMMIT;")
