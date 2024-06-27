#!/usr/local/bin/mnolth lua

local filename = arg[2]
local namespace = arg[1]

function basename(str)
    local name = string.gsub(str, "(.*/)(.*)", "%2")
    return name
end

local file_with_ns = namespace .. "/" .. basename(filename)

local textfiles_table = table.concat({
    "CREATE TABLE IF NOT EXISTS dz_textfiles(",
    "id INTEGER PRIMARY KEY,",
    "filename TEXT,",
    "linum INTEGER,",
    "data TEXT);"
}, "\n")

local clear_previous = table.concat({
    "DELETE FROM dz_textfiles WHERE filename is '",
    file_with_ns .. "';"
})

local fp = io.open(filename)
assert(fp ~= nil, "couldn't open: " .. filename)

print(textfiles_table)

function escape(str)
    return str:gsub("'", "''")
end

print("BEGIN;")
print(clear_previous)
local num = 1
for ln in fp:lines() do
    -- print(num, ln)
    print(table.concat({
        "INSERT INTO dz_textfiles(filename, linum, data)",
        "VALUES(",
        "'" .. file_with_ns .. "',",
        num .. ",",
        "'" .. escape(ln) .. "'",
        ");",
    }, "\n"))
    num = num + 1
end
print("COMMIT;")
fp:close()
