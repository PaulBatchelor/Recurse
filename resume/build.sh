> resume.db
cd ..
./tools/dagzet resume/resume.dz | sqlite3 resume/resume.db
cd -
mnolth lua resume.lua
pandoc -o out.html out.md
