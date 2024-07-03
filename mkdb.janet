# open and clear wiki db

(ww-open "a.db")
(ww-clear)

# unlinked pages

(ww-add-page "tasks" `@!(logparse/render-tasks-directory (ww-db))!@`)
(ww-add-page "logs" `#+TITLE: logs
I have developed a reasonably simple
text-based log format to keep
track of what I do day-to-day. These get parsed and turned
into SQLite tables, then those tables get presented here
in HTML.

@!(logparse/render-daily-logs (ww-db))!@
`)
(ww-add-page "dz/webdev/react" `@!(dagzet-page "data/webdev/react/index.json")!@`)
(ww-add-page "dz/webdev/wasm" `@!(dagzet-page "data/webdev/wasm/index.json")!@`)
(ww-add-page "dz/webdev" `@!(dagzet-page "data/webdev/index.json")!@`)
(ww-add-page "dz/web" `@!(dagzet-page "data/web/index.json")!@`)
(ww-add-page "dz/misc" `@!(dagzet-page "data/misc/index.json")!@`)
(ww-add-page "dz/reading/how_not_to_learn_rust" `@!(dagzet-page "data/reading/how_not_to_learn_rust/index.json")!@`)
(ww-add-page "dz/reading" `@!(dagzet-page "data/reading/index.json")!@`)
(ww-add-page "dz/gamedev/tic80" `@!(dagzet-page "data/gamedev/tic80/index.json")!@`)
(ww-add-page "dz/gamedev/pixelart" `@!(dagzet-page "data/gamedev/pixelart/index.json")!@`)
(ww-add-page "dz/gamedev/sokol" `@!(dagzet-page "data/gamedev/sokol/index.json")!@`)
(ww-add-page "dz/gamedev" `@!(dagzet-page "data/gamedev/index.json")!@`)
(ww-add-page "dz/planning/workflow_planning" `@!(dagzet-page "data/planning/workflow_planning/index.json")!@`)
(ww-add-page "dz/planning" `@!(dagzet-page "data/planning/index.json")!@`)
(ww-add-page "dz/voxbox" `@!(dagzet-page "data/voxbox/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/00_preface" `@!(dagzet-page "data/software_foundations/01_logical_foundations/00_preface/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/02_induction" `@!(dagzet-page "data/software_foundations/01_logical_foundations/02_induction/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/01_basics" `@!(dagzet-page "data/software_foundations/01_logical_foundations/01_basics/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations" `@!(dagzet-page "data/software_foundations/01_logical_foundations/index.json")!@`)
(ww-add-page "dz/software_foundations" `@!(dagzet-page "data/software_foundations/index.json")!@`)
(ww-add-page "dz/retrocomputing/next" `@!(dagzet-page "data/retrocomputing/next/index.json")!@`)
(ww-add-page "dz/retrocomputing" `@!(dagzet-page "data/retrocomputing/index.json")!@`)
(ww-add-page "dz/codestudy/hello_ts_react" `@!(dagzet-page "data/codestudy/hello_ts_react/index.json")!@`)
(ww-add-page "dz/codestudy/potential" `@!(dagzet-page "data/codestudy/potential/index.json")!@`)
(ww-add-page "dz/codestudy/rusty_bikes" `@!(dagzet-page "data/codestudy/rusty_bikes/index.json")!@`)
(ww-add-page "dz/codestudy" `@!(dagzet-page "data/codestudy/index.json")!@`)
(ww-add-page "dz/NTSC" `@!(dagzet-page "data/NTSC/index.json")!@`)
(ww-add-page "dz/rust/books/rust_by_example" `@!(dagzet-page "data/rust/books/rust_by_example/index.json")!@`)
(ww-add-page "dz/rust/books/cargo_book" `@!(dagzet-page "data/rust/books/cargo_book/index.json")!@`)
(ww-add-page "dz/rust/books/rust_book" `@!(dagzet-page "data/rust/books/rust_book/index.json")!@`)
(ww-add-page "dz/rust/books" `@!(dagzet-page "data/rust/books/index.json")!@`)
(ww-add-page "dz/rust/crates" `@!(dagzet-page "data/rust/crates/index.json")!@`)
(ww-add-page "dz/rust" `@!(dagzet-page "data/rust/index.json")!@`)
(ww-add-page "dz/FPGA" `@!(dagzet-page "data/FPGA/index.json")!@`)
(ww-add-page "dz/career" `@!(dagzet-page "data/career/index.json")!@`)
(ww-add-page "dz/recurse" `@!(dagzet-page "data/recurse/index.json")!@`)
(ww-add-page "dz/audio/pipewire" `@!(dagzet-page "data/audio/pipewire/index.json")!@`)
(ww-add-page "dz/audio" `@!(dagzet-page "data/audio/index.json")!@`)
(ww-add-page "dz" `@!(dagzet-page "data/index.json")!@`)
(ww-add-page "tasks/add_day_titles" `@!(logparse/render-logs-from-tag (ww-db) "add-day-titles")!@`)
(ww-add-page "tasks/add_demos_page" `@!(logparse/render-logs-from-tag (ww-db) "add-demos-page")!@`)
(ww-add-page "tasks/add_position_to_tasks" `@!(logparse/render-logs-from-tag (ww-db) "add-position-to-tasks")!@`)
(ww-add-page "tasks/add_tag_parser" `@!(logparse/render-logs-from-tag (ww-db) "add-tag-parser")!@`)
(ww-add-page "tasks/add_wasm_dz" `@!(logparse/render-logs-from-tag (ww-db) "add-wasm-dz")!@`)
(ww-add-page "tasks/blob_brainstorm" `@!(logparse/render-logs-from-tag (ww-db) "blob-brainstorm")!@`)
(ww-add-page "tasks/bucket_initial_scoping" `@!(logparse/render-logs-from-tag (ww-db) "bucket-initial-scoping")!@`)
(ww-add-page "tasks/bucket_storyboard" `@!(logparse/render-logs-from-tag (ww-db) "bucket-storyboard")!@`)
(ww-add-page "tasks/bug_missing_nodes" `@!(logparse/render-logs-from-tag (ww-db) "bug-missing-nodes")!@`)
(ww-add-page "tasks/building_rust_mentality" `@!(logparse/render-logs-from-tag (ww-db) "building-rust-mentality")!@`)
(ww-add-page "tasks/buy_extension_cord:" `@!(logparse/render-logs-from-tag (ww-db) "buy-extension-cord:")!@`)
(ww-add-page "tasks/chords_demo" `@!(logparse/render-logs-from-tag (ww-db) "chords-demo")!@`)
(ww-add-page "tasks/codeblocks_logs" `@!(logparse/render-logs-from-tag (ww-db) "codeblocks-logs")!@`)
(ww-add-page "tasks/compile_potential_vcv" `@!(logparse/render-logs-from-tag (ww-db) "compile-potential-vcv")!@`)
(ww-add-page "tasks/comprehensive_rust" `@!(logparse/render-logs-from-tag (ww-db) "comprehensive-rust")!@`)
(ww-add-page "tasks/connect_logs_to_tasks" `@!(logparse/render-logs-from-tag (ww-db) "connect-logs-to-tasks")!@`)
(ww-add-page "tasks/create_chatter_sounds" `@!(logparse/render-logs-from-tag (ww-db) "create-chatter-sounds")!@`)
(ww-add-page "tasks/create_dagzet_todo_page" `@!(logparse/render-logs-from-tag (ww-db) "create-dagzet-todo-page")!@`)
(ww-add-page "tasks/create_diams_interface" `@!(logparse/render-logs-from-tag (ww-db) "create-diams-interface")!@`)
(ww-add-page "tasks/create_tasks_directory" `@!(logparse/render-logs-from-tag (ww-db) "create-tasks-directory")!@`)
(ww-add-page "tasks/create_time_log_format" `@!(logparse/render-logs-from-tag (ww-db) "create-time-log-format")!@`)
(ww-add-page "tasks/dagzet_lists" `@!(logparse/render-logs-from-tag (ww-db) "dagzet-lists")!@`)
(ww-add-page "tasks/demo_crossfade_shapes" `@!(logparse/render-logs-from-tag (ww-db) "demo-crossfade-shapes")!@`)
(ww-add-page "tasks/demo_ensemble" `@!(logparse/render-logs-from-tag (ww-db) "demo-ensemble")!@`)
(ww-add-page "tasks/demo_poke" `@!(logparse/render-logs-from-tag (ww-db) "demo-poke")!@`)
(ww-add-page "tasks/demo_preset_export" `@!(logparse/render-logs-from-tag (ww-db) "demo-preset-export")!@`)
(ww-add-page "tasks/demo_react_UI" `@!(logparse/render-logs-from-tag (ww-db) "demo-react-UI")!@`)
(ww-add-page "tasks/demo_tongue_control" `@!(logparse/render-logs-from-tag (ww-db) "demo-tongue-control")!@`)
(ww-add-page "tasks/dzgraph_hyperlinks" `@!(logparse/render-logs-from-tag (ww-db) "dzgraph-hyperlinks")!@`)
(ww-add-page "tasks/effective_rust" `@!(logparse/render-logs-from-tag (ww-db) "effective-rust")!@`)
(ww-add-page "tasks/game_jam" `@!(logparse/render-logs-from-tag (ww-db) "game-jam")!@`)
(ww-add-page "tasks/how_not_to_learn_rust" `@!(logparse/render-logs-from-tag (ww-db) "how-not-to-learn-rust")!@`)
(ww-add-page "tasks/html_task_descriptions" `@!(logparse/render-logs-from-tag (ww-db) "html-task-descriptions")!@`)
(ww-add-page "tasks/htmlize_codestudy_files" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-codestudy-files")!@`)
(ww-add-page "tasks/htmlize_knowledge_tree" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-knowledge-tree")!@`)
(ww-add-page "tasks/htmlize_logs" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-logs")!@`)
(ww-add-page "tasks/htmlize_tasks" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-tasks")!@`)
(ww-add-page "tasks/implement_DRM" `@!(logparse/render-logs-from-tag (ww-db) "implement-DRM")!@`)
(ww-add-page "tasks/implement_gesture_path" `@!(logparse/render-logs-from-tag (ww-db) "implement-gesture-path")!@`)
(ww-add-page "tasks/implement_glot" `@!(logparse/render-logs-from-tag (ww-db) "implement-glot")!@`)
(ww-add-page "tasks/implement_monowav" `@!(logparse/render-logs-from-tag (ww-db) "implement-monowav")!@`)
(ww-add-page "tasks/implement_mtof" `@!(logparse/render-logs-from-tag (ww-db) "implement-mtof")!@`)
(ww-add-page "tasks/implement_osc" `@!(logparse/render-logs-from-tag (ww-db) "implement-osc")!@`)
(ww-add-page "tasks/implement_phasor" `@!(logparse/render-logs-from-tag (ww-db) "implement-phasor")!@`)
(ww-add-page "tasks/implement_rephasor" `@!(logparse/render-logs-from-tag (ww-db) "implement-rephasor")!@`)
(ww-add-page "tasks/implement_smoother" `@!(logparse/render-logs-from-tag (ww-db) "implement-smoother")!@`)
(ww-add-page "tasks/implement_tract" `@!(logparse/render-logs-from-tag (ww-db) "implement-tract")!@`)
(ww-add-page "tasks/implement_velum" `@!(logparse/render-logs-from-tag (ww-db) "implement-velum")!@`)
(ww-add-page "tasks/impossible_day" `@!(logparse/render-logs-from-tag (ww-db) "impossible-day")!@`)
(ww-add-page "tasks/initial_singing_web" `@!(logparse/render-logs-from-tag (ww-db) "initial-singing-web")!@`)
(ww-add-page "tasks/initial_voxbox_repo" `@!(logparse/render-logs-from-tag (ww-db) "initial-voxbox-repo")!@`)
(ww-add-page "tasks/investigate_2d_gameengine" `@!(logparse/render-logs-from-tag (ww-db) "investigate-2d-gameengine")!@`)
(ww-add-page "tasks/investigate_kickstart_neovim" `@!(logparse/render-logs-from-tag (ww-db) "investigate-kickstart-neovim")!@`)
(ww-add-page "tasks/investigate_tic80" `@!(logparse/render-logs-from-tag (ww-db) "investigate-tic80")!@`)
(ww-add-page "tasks/investigate_wabt" `@!(logparse/render-logs-from-tag (ww-db) "investigate-wabt")!@`)
(ww-add-page "tasks/leaving_rust_gamedev" `@!(logparse/render-logs-from-tag (ww-db) "leaving-rust-gamedev")!@`)
(ww-add-page "tasks/log_sqlite_gen" `@!(logparse/render-logs-from-tag (ww-db) "log-sqlite-gen")!@`)
(ww-add-page "tasks/logging_presentation" `@!(logparse/render-logs-from-tag (ww-db) "logging-presentation")!@`)
(ww-add-page "tasks/morning_triage" `@!(logparse/render-logs-from-tag (ww-db) "morning-triage")!@`)
(ww-add-page "tasks/mplayer_jack_thinkpad" `@!(logparse/render-logs-from-tag (ww-db) "mplayer-jack-thinkpad")!@`)
(ww-add-page "tasks/nexthacking" `@!(logparse/render-logs-from-tag (ww-db) "nexthacking")!@`)
(ww-add-page "tasks/procedural_macros_rust" `@!(logparse/render-logs-from-tag (ww-db) "procedural-macros-rust")!@`)
(ww-add-page "tasks/project_outline" `@!(logparse/render-logs-from-tag (ww-db) "project-outline")!@`)
(ww-add-page "tasks/provision_thinkpad" `@!(logparse/render-logs-from-tag (ww-db) "provision-thinkpad")!@`)
(ww-add-page "tasks/quick_preset_export" `@!(logparse/render-logs-from-tag (ww-db) "quick-preset-export")!@`)
(ww-add-page "tasks/rc_jobs_advice" `@!(logparse/render-logs-from-tag (ww-db) "rc-jobs-advice")!@`)
(ww-add-page "tasks/react_adding_interactivity" `@!(logparse/render-logs-from-tag (ww-db) "react-adding-interactivity")!@`)
(ww-add-page "tasks/react_describing_the_ui" `@!(logparse/render-logs-from-tag (ww-db) "react-describing-the-ui")!@`)
(ww-add-page "tasks/react_escape_hatches" `@!(logparse/render-logs-from-tag (ww-db) "react-escape-hatches")!@`)
(ww-add-page "tasks/react_first_component" `@!(logparse/render-logs-from-tag (ww-db) "react-first-component")!@`)
(ww-add-page "tasks/react_installation" `@!(logparse/render-logs-from-tag (ww-db) "react-installation")!@`)
(ww-add-page "tasks/react_managing_state" `@!(logparse/render-logs-from-tag (ww-db) "react-managing-state")!@`)
(ww-add-page "tasks/react_quickstart" `@!(logparse/render-logs-from-tag (ww-db) "react-quickstart")!@`)
(ww-add-page "tasks/react_thinking_in_react" `@!(logparse/render-logs-from-tag (ww-db) "react-thinking-in-react")!@`)
(ww-add-page "tasks/react_tic_tac_toe" `@!(logparse/render-logs-from-tag (ww-db) "react-tic-tac-toe")!@`)
(ww-add-page "tasks/refactor_glotfilt_traits" `@!(logparse/render-logs-from-tag (ww-db) "refactor-glotfilt-traits")!@`)
(ww-add-page "tasks/resume_setup" `@!(logparse/render-logs-from-tag (ww-db) "resume-setup")!@`)
(ww-add-page "tasks/revisit_isorhythms" `@!(logparse/render-logs-from-tag (ww-db) "revisit-isorhythms")!@`)
(ww-add-page "tasks/revisit_rust_wasm_audioworklet" `@!(logparse/render-logs-from-tag (ww-db) "revisit-rust-wasm-audioworklet")!@`)
(ww-add-page "tasks/rework_rectangles" `@!(logparse/render-logs-from-tag (ww-db) "rework-rectangles")!@`)
(ww-add-page "tasks/rust_neovim_setup" `@!(logparse/render-logs-from-tag (ww-db) "rust-neovim-setup")!@`)
(ww-add-page "tasks/rust_project_setup" `@!(logparse/render-logs-from-tag (ww-db) "rust-project-setup")!@`)
(ww-add-page "tasks/set_up_rust_reading_list" `@!(logparse/render-logs-from-tag (ww-db) "set-up-rust-reading-list")!@`)
(ww-add-page "tasks/site_debugging_jun30" `@!(logparse/render-logs-from-tag (ww-db) "site-debugging-jun30")!@`)
(ww-add-page "tasks/study_rusty_bikes" `@!(logparse/render-logs-from-tag (ww-db) "study-rusty-bikes")!@`)
(ww-add-page "tasks/study_synthkit" `@!(logparse/render-logs-from-tag (ww-db) "study-synthkit")!@`)
(ww-add-page "tasks/study_termimad" `@!(logparse/render-logs-from-tag (ww-db) "study-termimad")!@`)
(ww-add-page "tasks/task_sqlite_gen" `@!(logparse/render-logs-from-tag (ww-db) "task-sqlite-gen")!@`)
(ww-add-page "tasks/task_system_setup" `@!(logparse/render-logs-from-tag (ww-db) "task-system-setup")!@`)
(ww-add-page "tasks/test_dz_log_task_linking" `@!(logparse/render-logs-from-tag (ww-db) "test-dz-log-task-linking")!@`)
(ww-add-page "tasks/thinkpad_uploader" `@!(logparse/render-logs-from-tag (ww-db) "thinkpad-uploader")!@`)
(ww-add-page "tasks/toc_logs" `@!(logparse/render-logs-from-tag (ww-db) "toc-logs")!@`)
(ww-add-page "tasks/too_many_linked_lists" `@!(logparse/render-logs-from-tag (ww-db) "too-many-linked-lists")!@`)
(ww-add-page "tasks/troubleshoot_webaudio_thinkpad" `@!(logparse/render-logs-from-tag (ww-db) "troubleshoot-webaudio-thinkpad")!@`)
(ww-add-page "tasks/typescript_react_slider" `@!(logparse/render-logs-from-tag (ww-db) "typescript-react-slider")!@`)
(ww-add-page "tasks/vcv_potential_study" `@!(logparse/render-logs-from-tag (ww-db) "vcv-potential-study")!@`)
(ww-add-page "tasks/vocal_chords_older_iphone" `@!(logparse/render-logs-from-tag (ww-db) "vocal-chords-older-iphone")!@`)
(ww-add-page "tasks/voxbox_better_size_control" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-better-size-control")!@`)
(ww-add-page "tasks/voxbox_change_nose_length" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-change-nose-length")!@`)
(ww-add-page "tasks/voxbox_dsp_tasks" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-dsp-tasks")!@`)
(ww-add-page "tasks/voxbox_linear_gesture_demo" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-linear-gesture-demo")!@`)
(ww-add-page "tasks/voxbox_shape_morphing" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-shape-morphing")!@`)
(ww-add-page "tasks/voxbox_size_control" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-size-control")!@`)
(ww-add-page "tasks/voxbox_tongue_interface" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-tongue-interface")!@`)
(ww-add-page "tasks/voxbox_vcv" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-vcv")!@`)
(ww-add-page "tasks/voxboxOSC" `@!(logparse/render-logs-from-tag (ww-db) "voxboxOSC")!@`)
(ww-add-page "tasks/vscode_rust_setup" `@!(logparse/render-logs-from-tag (ww-db) "vscode-rust-setup")!@`)
(ww-add-page "tasks/what_now_week6" `@!(logparse/render-logs-from-tag (ww-db) "what-now-week6")!@`)
(ww-add-page "tasks/what_now_week7" `@!(logparse/render-logs-from-tag (ww-db) "what-now-week7")!@`)
(ww-add-page "taskgroups/DSP" `@!(logparse/render-tasks-from-group (ww-db) "DSP")!@`)
(ww-add-page "taskgroups/code_study" `@!(logparse/render-tasks-from-group (ww-db) "code_study")!@`)
(ww-add-page "taskgroups/done" `@!(logparse/render-tasks-from-group (ww-db) "done")!@`)
(ww-add-page "taskgroups/main" `@!(logparse/render-tasks-from-group (ww-db) "main")!@`)
(ww-add-page "taskgroups/priority" `@!(logparse/render-tasks-from-group (ww-db) "priority")!@`)
(ww-add-page "taskgroups/reading" `@!(logparse/render-tasks-from-group (ww-db) "reading")!@`)
(ww-add-page "taskgroups/rust" `@!(logparse/render-tasks-from-group (ww-db) "rust")!@`)
(ww-add-page "taskgroups/voxbox" `@!(logparse/render-tasks-from-group (ww-db) "voxbox")!@`)
(ww-add-page "taskgroups/web" `@!(logparse/render-tasks-from-group (ww-db) "web")!@`)
(ww-add-page "taskgroups" `@!(logparse/render-taskgroups-directory (ww-db))!@`)
(ww-add-page "dzf/codestudy/potential/plugin.hpp" `@!(genhtml/textlines "codestudy/potential/plugin.hpp")!@`)
(ww-add-page "dzf/codestudy/potential/build.rs" `@!(genhtml/textlines "codestudy/potential/build.rs")!@`)
(ww-add-page "dzf/codestudy/potential/mag_sign.cpp" `@!(genhtml/textlines "codestudy/potential/mag_sign.cpp")!@`)
(ww-add-page "dzf/codestudy/potential/mag_sign.rs" `@!(genhtml/textlines "codestudy/potential/mag_sign.rs")!@`)
(ww-add-page "dzf/codestudy/potential/module_config.rs" `@!(genhtml/textlines "codestudy/potential/module_config.rs")!@`)
(ww-add-page "dzf/codestudy/potential/plugin.cpp" `@!(genhtml/textlines "codestudy/potential/plugin.cpp")!@`)
(ww-add-page "dzf/codestudy/potential/rack.rs" `@!(genhtml/textlines "codestudy/potential/rack.rs")!@`)
(ww-add-page "dzf/codestudy/hello_ts_react/App.css" `@!(genhtml/textlines "codestudy/hello_ts_react/App.css")!@`)
(ww-add-page "dzf/codestudy/hello_ts_react/App.test.tsx" `@!(genhtml/textlines "codestudy/hello_ts_react/App.test.tsx")!@`)
(ww-add-page "dzf/codestudy/hello_ts_react/App.tsx" `@!(genhtml/textlines "codestudy/hello_ts_react/App.tsx")!@`)
(ww-add-page "dzf/codestudy/hello_ts_react/index.tsx" `@!(genhtml/textlines "codestudy/hello_ts_react/index.tsx")!@`)

# linked pages

(ww-add-link "index" "wiki/index.org")
(ww-add-link "demos" "wiki/demos.org")
(ww-add-link "how_logging_works" "wiki/how_logging_works.org")
(ww-add-link "logging_overview" "wiki/logging_overview.org")
(ww-add-link "logging_pipeline" "wiki/logging_pipeline.org")
(ww-add-link "site_ecosystem" "wiki/site_ecosystem.org")
(ww-add-link "logging_format" "wiki/logging_format.org")
(ww-add-link "week07" "wiki/week07.org")

# sync and close

(ww-sync)
(ww-close)
