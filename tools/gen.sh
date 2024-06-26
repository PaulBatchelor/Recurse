# generate dagzet and wiki pages
./tools/gendb.sh
./tools/dz_wikigen.sh

# generate logs
./tools/genlogdb.sh

# generate tasks and wiki pages
./tools/gentasks.sh
./tools/generate_task_pages.sh
./tools/generate_taskgroup_pages.sh

# code study
./tools/import_codestudy.sh

# to be called after dagzet is created
./tools/gendzfiles.sh

