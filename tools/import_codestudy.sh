LUA="mnolth lua"
function import_code() {
    NAMESPACE=$1
    FILENAME=$2
    echo "codestudy $NAMESPACE $FILENAME"
    $LUA \
        tools/import_file.lua \
        $NAMESPACE codestudy/$FILENAME | sqlite3 a.db
}

import_code codestudy/potential potential/plugin.hpp
import_code codestudy/potential potential/plugin.cpp
import_code codestudy/potential potential/build.rs
import_code codestudy/potential potential/mag_sign.cpp
import_code codestudy/potential potential/mag_sign.rs
import_code codestudy/potential potential/module_config.rs
import_code codestudy/potential potential/plugin.cpp
import_code codestudy/potential potential/rack.rs
