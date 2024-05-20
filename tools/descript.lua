Descript = {}
function split(val, sep)
    local sep = lpeg.P(sep)
    local elem = lpeg.C((1 - sep)^0)
    local lines = elem * (sep * elem)^0
    lines = lpeg.Ct(lines)
    return lpeg.match(lines, val)
end

function atfun (subject, pos, vals)
    local split_vals = split(vals, '\n')

    local new_vals = {}

    for i,v in pairs(split_vals) do
        if #v > 0 and string.byte(v, 1) ~= string.byte('#')  then
            table.insert(new_vals, v)
        end
    end

    if #new_vals == 0 then return true end
    return true, new_vals
end

function Descript.parse(str)
    local atsym = lpeg.P("@")
    local atelem = lpeg.C((1 - atsym)^0)
    local atelem = lpeg.Cmt(atelem, atfun)
    local atblock = (atsym * atelem)^0 * atelem
    local t = lpeg.match(lpeg.Ct(atblock), str)
    return t
end
return Descript
