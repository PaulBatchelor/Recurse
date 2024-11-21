# generate dagzet and wiki pages
./tools/gendb.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi
./tools/dz_wikigen.sh
if [[ ! $? -eq 0 ]]
then
    exit 1
fi
./tools/import_codestudy.sh
./tools/gendzfiles.sh

