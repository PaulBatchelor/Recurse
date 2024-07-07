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


import_code codestudy/hello_ts_react hello_ts_react/App.css
import_code codestudy/hello_ts_react hello_ts_react/App.test.tsx
import_code codestudy/hello_ts_react hello_ts_react/App.tsx
import_code codestudy/hello_ts_react hello_ts_react/index.tsx

import_code codestudy/tic80 tic80/sound.c
import_code codestudy/tic80 tic80/tic.c
import_code codestudy/tic80 tic80/studio.c
