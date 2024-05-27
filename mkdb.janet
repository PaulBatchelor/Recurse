# open and clear wiki db

(ww-open "a.db")
(ww-clear)

# unlinked pages

(ww-add-page "logs" `#+TITLE: logs
I have developed a reasonably simple
text-based log format to keep
track of what I do day-to-day. These get parsed and turned
into SQLite tables, then those tables get presented here
in HTML.

@!(logparse/render-daily-logs (ww-db))!@`)
(ww-add-page "dz/career" `@!(dagzet-page "data/career/index.json")!@`)
(ww-add-page "dz/reading/how_not_to_learn_rust" `@!(dagzet-page "data/reading/how_not_to_learn_rust/index.json")!@`)
(ww-add-page "dz/reading" `@!(dagzet-page "data/reading/index.json")!@`)
(ww-add-page "dz/misc" `@!(dagzet-page "data/misc/index.json")!@`)
(ww-add-page "dz/planning/workflow_planning" `@!(dagzet-page "data/planning/workflow_planning/index.json")!@`)
(ww-add-page "dz/planning" `@!(dagzet-page "data/planning/index.json")!@`)
(ww-add-page "dz/rust/libs" `@!(dagzet-page "data/rust/libs/index.json")!@`)
(ww-add-page "dz/rust/books/cargo_book" `@!(dagzet-page "data/rust/books/cargo_book/index.json")!@`)
(ww-add-page "dz/rust/books/rust_by_example" `@!(dagzet-page "data/rust/books/rust_by_example/index.json")!@`)
(ww-add-page "dz/rust/books" `@!(dagzet-page "data/rust/books/index.json")!@`)
(ww-add-page "dz/rust" `@!(dagzet-page "data/rust/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/00_preface" `@!(dagzet-page "data/software_foundations/01_logical_foundations/00_preface/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/02_induction" `@!(dagzet-page "data/software_foundations/01_logical_foundations/02_induction/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations/01_basics" `@!(dagzet-page "data/software_foundations/01_logical_foundations/01_basics/index.json")!@`)
(ww-add-page "dz/software_foundations/01_logical_foundations" `@!(dagzet-page "data/software_foundations/01_logical_foundations/index.json")!@`)
(ww-add-page "dz/software_foundations" `@!(dagzet-page "data/software_foundations/index.json")!@`)
(ww-add-page "dz/web" `@!(dagzet-page "data/web/index.json")!@`)
(ww-add-page "dz" `@!(dagzet-page "data/index.json")!@`)
(ww-add-page "tasks/add_position_to_tasks" `@!(logparse/render-logs-from-tag (ww-db) "add-position-to-tasks")!@`)
(ww-add-page "tasks/add_tag_parser" `@!(logparse/render-logs-from-tag (ww-db) "add-tag-parser")!@`)
(ww-add-page "tasks/building_rust_mentality" `@!(logparse/render-logs-from-tag (ww-db) "building-rust-mentality")!@`)
(ww-add-page "tasks/codeblocks_logs" `@!(logparse/render-logs-from-tag (ww-db) "codeblocks-logs")!@`)
(ww-add-page "tasks/comprehensive_rust" `@!(logparse/render-logs-from-tag (ww-db) "comprehensive-rust")!@`)
(ww-add-page "tasks/connect_logs_to_tasks" `@!(logparse/render-logs-from-tag (ww-db) "connect-logs-to-tasks")!@`)
(ww-add-page "tasks/create_time_log_format" `@!(logparse/render-logs-from-tag (ww-db) "create-time-log-format")!@`)
(ww-add-page "tasks/effective_rust" `@!(logparse/render-logs-from-tag (ww-db) "effective-rust")!@`)
(ww-add-page "tasks/how_not_to_learn_rust" `@!(logparse/render-logs-from-tag (ww-db) "how-not-to-learn-rust")!@`)
(ww-add-page "tasks/htmlize_knowledge_tree" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-knowledge-tree")!@`)
(ww-add-page "tasks/htmlize_logs" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-logs")!@`)
(ww-add-page "tasks/htmlize_tasks" `@!(logparse/render-logs-from-tag (ww-db) "htmlize-tasks")!@`)
(ww-add-page "tasks/impl_gesture_path" `@!(logparse/render-logs-from-tag (ww-db) "impl-gesture-path")!@`)
(ww-add-page "tasks/implement_DRM" `@!(logparse/render-logs-from-tag (ww-db) "implement-DRM")!@`)
(ww-add-page "tasks/implement_glot" `@!(logparse/render-logs-from-tag (ww-db) "implement-glot")!@`)
(ww-add-page "tasks/implement_monowav" `@!(logparse/render-logs-from-tag (ww-db) "implement-monowav")!@`)
(ww-add-page "tasks/implement_osc" `@!(logparse/render-logs-from-tag (ww-db) "implement-osc")!@`)
(ww-add-page "tasks/implement_phasor" `@!(logparse/render-logs-from-tag (ww-db) "implement-phasor")!@`)
(ww-add-page "tasks/implement_rephasor" `@!(logparse/render-logs-from-tag (ww-db) "implement-rephasor")!@`)
(ww-add-page "tasks/implement_tract" `@!(logparse/render-logs-from-tag (ww-db) "implement-tract")!@`)
(ww-add-page "tasks/initial_voxbox_repo" `@!(logparse/render-logs-from-tag (ww-db) "initial-voxbox-repo")!@`)
(ww-add-page "tasks/leaving_rust_gamedev" `@!(logparse/render-logs-from-tag (ww-db) "leaving-rust-gamedev")!@`)
(ww-add-page "tasks/log_sqlite_gen" `@!(logparse/render-logs-from-tag (ww-db) "log-sqlite-gen")!@`)
(ww-add-page "tasks/plan_reading_schedule" `@!(logparse/render-logs-from-tag (ww-db) "plan-reading-schedule")!@`)
(ww-add-page "tasks/procedural_macros_rust" `@!(logparse/render-logs-from-tag (ww-db) "procedural-macros-rust")!@`)
(ww-add-page "tasks/project_outline" `@!(logparse/render-logs-from-tag (ww-db) "project-outline")!@`)
(ww-add-page "tasks/rc_jobs_advice" `@!(logparse/render-logs-from-tag (ww-db) "rc-jobs-advice")!@`)
(ww-add-page "tasks/resume_setup" `@!(logparse/render-logs-from-tag (ww-db) "resume-setup")!@`)
(ww-add-page "tasks/revisit_isorhythms" `@!(logparse/render-logs-from-tag (ww-db) "revisit-isorhythms")!@`)
(ww-add-page "tasks/revisit_rust_wasm_audioworklet" `@!(logparse/render-logs-from-tag (ww-db) "revisit-rust-wasm-audioworklet")!@`)
(ww-add-page "tasks/rust_project_setup" `@!(logparse/render-logs-from-tag (ww-db) "rust-project-setup")!@`)
(ww-add-page "tasks/set_up_rust_reading_list" `@!(logparse/render-logs-from-tag (ww-db) "set-up-rust-reading-list")!@`)
(ww-add-page "tasks/study_termimad" `@!(logparse/render-logs-from-tag (ww-db) "study-termimad")!@`)
(ww-add-page "tasks/task_sqlite_gen" `@!(logparse/render-logs-from-tag (ww-db) "task-sqlite-gen")!@`)
(ww-add-page "tasks/task_system_setup" `@!(logparse/render-logs-from-tag (ww-db) "task-system-setup")!@`)
(ww-add-page "tasks/too_many_linked_lists" `@!(logparse/render-logs-from-tag (ww-db) "too-many-linked-lists")!@`)
(ww-add-page "tasks/voxbox_dsp_tasks" `@!(logparse/render-logs-from-tag (ww-db) "voxbox-dsp-tasks")!@`)
(ww-add-page "tasks/vscode_rust_setup" `@!(logparse/render-logs-from-tag (ww-db) "vscode-rust-setup")!@`)
(ww-add-page "taskgroups/DSP" `@!(logparse/render-tasks-from-group (ww-db) "DSP")!@`)
(ww-add-page "taskgroups/code_study" `@!(logparse/render-tasks-from-group (ww-db) "code_study")!@`)
(ww-add-page "taskgroups/done" `@!(logparse/render-tasks-from-group (ww-db) "done")!@`)
(ww-add-page "taskgroups/main" `@!(logparse/render-tasks-from-group (ww-db) "main")!@`)
(ww-add-page "taskgroups/priority" `@!(logparse/render-tasks-from-group (ww-db) "priority")!@`)
(ww-add-page "taskgroups/reading" `@!(logparse/render-tasks-from-group (ww-db) "reading")!@`)
(ww-add-page "taskgroups/rust" `@!(logparse/render-tasks-from-group (ww-db) "rust")!@`)
(ww-add-page "taskgroups" `@!(logparse/render-taskgroups-directory (ww-db))!@`)

# linked pages

(ww-add-link "index" "wiki/index.org")

# sync and close

(ww-sync)
(ww-close)
