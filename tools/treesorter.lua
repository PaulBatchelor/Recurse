-- treesorter: this function recursively sorts the branches
-- of a generated tree

treesorter = {}

function tree_comp(a, b)
    return a[1] < b[1]
end

function tree_keys(tree)
    local keys = {}

    -- extract keys at one level, subtrees will
    -- just be the name of top-level node
    for pos, node in pairs(tree) do
        if type(node) == "string" then
            table.insert(keys, {string.lower(node), pos})
        else
            table.insert(keys, {string.lower(node[1]), pos})
        end
    end

    -- keys is sorted by page name, but their relative
    -- position in the original list is stored
    table.sort(keys, tree_comp)

    --- only the indices are needed: tree[key_index[i]]
    key_index = {}

    for _, v in pairs(keys) do
        table.insert(key_index, v[2])
    end

    return key_index
end

function treesorter.treesorter(tree)
    local tk = tree_keys(tree)
    local new_tree = {}

    for _,v in pairs(tk) do
        local node = tree[v]
        if type(node) == "table" then
            --- tree syntax: [name, [children]], where
            --- children are more trees.
            --- recursively sort the trees
            node[2] = treesorter.treesorter(node[2])
        end
        table.insert(new_tree, node)
    end

    return new_tree
end

-- json = require("tools/json")
-- 
-- tree = io.open("tree.json")
-- tree = tree:read("*all")
-- tree = json.decode(tree)
-- 
-- new_tree = treesorter.treesorter(tree)
-- print(json.encode(new_tree))

setmetatable(treesorter, {
    __call = function (_, ...)
        treesorter.treesorter(...)
    end
})

return treesorter
