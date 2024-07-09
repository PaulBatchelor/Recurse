
#ARCHIVE_URL="https://web.archive.org/web/20230608045704/https://leetcode.com/problems/merge-strings-alternately/description/"

#chromium --headless --print-to-pdf https://leetcode.com/problems/merge-strings-alternately/
#chromium --headless --print-to-pdf $ARCHIVE_URL
#curl https://leetcode.com/problems/merge-strings-alternately/desription
#w3m https://leetcode.com/problems/merge-strings-alternately/desription

ARCHIVE_URL=$(curl http://archive.org/wayback/available?url=leetcode.com/problems/merge-strings-alternately/description/ |\
    jq -r '.archived_snapshots.closest.url')

curl -o page.html $ARCHIVE_URL 

