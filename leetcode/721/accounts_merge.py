# 2024-10-14: This passed the edge case, but I'm doing
# a lot of copying to get the merging correct. This feels
# like the sort of thing a database would do, but it
# also seems inefficient

class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        merged = {}
        for row in accounts:
            name = row[0]
            emails = set(row[1:])
            merge_idx = []
            if name in merged:
                # check and see if there's any intersection, and merge the sets
                for i in range(0, len(merged[name])):
                        email_row = merged[name][i]
                        # multiple intersections possible, which would inidicate multiple merges
                        if emails & email_row:
                            merge_idx.append(i)
                            #merged[name][i] |= emails
                if len(merge_idx) > 0:
                    new_emails = set(emails)
                    for idx in merge_idx:
                        new_emails |=  merged[name][idx]
                        # tombstone, to be overwritten later
                        merged[name][idx] = None
                    new_email_list = []
                    # create new email list, skipping the merged lists
                    for email in merged[name]:
                        if email is None:
                            continue
                        new_email_list.append(email)
                    new_email_list.append(new_emails)
                    merged[name] = new_email_list
                    #merged[name][merge_idx[0]] |= emails
                else:
                    merged[name].append(emails)
            else:
                merged[name] = [emails]
        merged_out = []
        for name, users in merged.items():
            for user_emails in users:
                merged_out.append([name] + sorted(user_emails))
        
        return merged_out

