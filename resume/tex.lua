local function prelude()
    local t = {
        "\\input color",
        "\\nopagenumbers",
        "\\parindent=0pt",

        "\\font\\headerfont=cmss17 at 34pt",
        "\\font\\subheaderfont=cmss17 at 24pt",
        "\\font\\sectionfont =cmssbx10 at 17pt",
        "\\font\\regularfont=cmss10 at 12pt",
        "\\font\\regularfontbold=cmssbx10 at 12pt",

        "\\definecolor{lightblue}{RGB}{0,150,255}",
        "\\definecolor{lightgrey}{RGB}{110,110,110}",

        "\\def\\section#1{",
        "\\sectionfont {#1}",
        "}",

        "\\def\\entry#1#2#3{",
        "{\\regularfontbold #1}",
        "{\\regularfont \\textcolor{lightgrey}{#2}}",
        "\\hfill \\textcolor{lightblue}{#3}",
        "\\smallskip",
        "{\\color{lightgrey} \\hrule }",
        "\\smallskip",
        "}",
    }
    return table.concat(t, "\n")
end

function epilogue()
    return "\\bye"
end

function header1(str)
    return
        "\\centerline{\\headerfont " .. str .."}\n" ..
        "\\smallskip"
end

function header2(str)
    return "\\section{" .. str .. "}\n\\medskip\n"
end

function header3(str)
    return "\\entry{" .. str .. "}{}{}\n"
end

function begin_list()
    return "\\regularfont"
end

function end_list()
    return ""
end

function item(str)
    return
        "\\quad $\\bullet$\n" ..
        str ..
        "\\smallskip"
end

return {
    prelude = prelude,

    epilogue = epilogue,

    header1 = header1,

    header2 = header2,

    header3 = header3,

    begin_list = begin_list,

    end_list = end_list,

    item = item,
}
