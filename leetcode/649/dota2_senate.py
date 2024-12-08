# 2024-12-08 Got it working with one queue and ban counts,
# the Claude solution using two queues had this little trick
# with adding offsets that was clever

from collections import deque
class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        radiant = deque()
        dire = deque()

        for i in range(len(senate)):
            if senate[i] == 'R':
                radiant.append(i)
            else:
                dire.append(i)

        while radiant and dire:
            ridx = radiant.popleft()
            didx = dire.popleft()

            if ridx < didx:
                # this is really clever. wouldn't have
                # gotten this
                radiant.append(ridx + len(senate))
            else:
                dire.append(didx + len(senate))
        return "Radiant" if radiant else "Dire"
    # initial solution:
    # multiple bans can happen, so use a ban counter instead
    # of a boolean
    def predictPartyVictoryV1(self, senate: str) -> str:
        # push R/D onto initial queue, keep counts
        q = deque()
        rcount = 0
        dcount = 0
        rban = 0
        dban = 0
        for s in senate:
            q.append(s)
            if s == 'R':
                rcount += 1
            else:
                dcount += 1
        # while queue is greater than 1
        while len(q) > 1:
            newq = deque()
            while q:
                #   - pop off the current senator, determine party
                cur = q.popleft()
                #   - check the rival count, if zero, return victory
                rival_count = rcount if cur == 'D' else dcount
                if rival_count == 0:
                    return "Radiant" if cur == 'R' else "Dire"

                #   - if banned flag on, do not push onto new queue,
                #     decrease count
                if cur == 'R' and rban > 0:
                    rban -= 1
                    continue
                elif cur == 'D' and dban > 0:
                    dban -= 1
                    continue
                #   - if rival count non-zero, turn on ban flag,
                #     push onto stack
                if cur == 'R':
                    dcount -= 1
                    dban += 1
                    newq.append(cur)
                    continue
                if cur == 'D':
                    rcount -= 1
                    rban += 1
                    newq.append(cur)
                    continue
            #   - assign new
            q = newq


        # return last item in queue
        return "Dire" if q[0] == 'D' else "Radiant"
