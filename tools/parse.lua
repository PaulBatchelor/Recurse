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
dash = "-"
comment = lpeg.P(" ")^0 * lpeg.Cg(lpeg.Cp(), "comment_start")

date = lpeg.Ct(year * dash * month * dash * day * comment)

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
            title = string.sub(str, t.comment_start)
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

for d,e in pairs(events) do
    print("Day: " .. d)
    if(e.comment) then print(table.concat(e.comment, " ")) end

    for pos,evt in pairs(e.events) do
        print(string.format("%02d: %s %s", pos, evt.time, evt.title))
        if(evt.comment) then print(table.concat(evt.comment, " ")) end
    end
end
