import random
import queue


class Maze:
    def __init__(self, m=30, n=40, N = 80):
        if m>N or n>N:
            exit()
        self.R = [[False for col in range(N)] for row in range(N)]
        self.D = [[False for col in range(N)] for row in range(N)]
        self.v = [[False for col in range(N)] for row in range(N)]
        self.row = [-1, 0, 1, 0]
        self.col = [0, -1, 0, 1]
        self.m = m
        self.n = n

    def dfs_generate(self, start_dim=(0, 0)):
        r = start_dim[0]
        c = start_dim[1]
        self.dfs(r, c)

    def dfs(self, r, c):
        d = random.randrange(0, 4)
        tmp = random.randrange(0, 2)
        dd = 1 if tmp == 1 else 3
        self.v[r][c] = True
        for i in range(4):
            rr = r + self.row[d]
            cc = c + self.col[d]
            if (rr >= 0 and rr < self.m) and (cc >= 0 and cc < self.n) and self.v[rr][cc] == False:
                # print("?")
                if d % 2 == 1:
                    self.R[r][c - (d == 1)] = True
                else:
                    self.D[r - (d == 0)][c] = True
                self.dfs(rr, cc)
            d = (d + dd) % 4

    # try not to use this, it's awful
    def bfs_generate(self, start_dim=(0, 0)):
        q = queue.Queue()
        q.put(start_dim)
        have_visited = 0
        self.v[start_dim[0]][start_dim[1]] = True
        while have_visited<self.m*self.n:
            cur_dim = q.get()
            have_visited += 1
            r = cur_dim[0]
            c = cur_dim[1]
            d = random.randrange(0, 4)
            tmp = random.randrange(0, 2)
            dd = 1 if tmp == 1 else 3
            # print(d, dd)
            for i in range(4):
                rr = r + self.row[d]
                cc = c + self.col[d]
                if (rr >= 0 and rr < self.m) and (cc >= 0 and cc < self.n) and self.v[rr][cc] == False:
                    q.put((rr, cc))
                    self.v[rr][cc] = True
                    if d % 2 == 1:
                        self.R[r][c - (d == 1)] = True
                    else:
                        self.D[r - (d == 0)][c] = True
                d = (d + dd) % 4

    def random_kruskal_generate(self):
        # the simplest algorithm to realize kruskal
        dots = []
        sets = []
        for i in range(self.m):
            for j in range(self.n):
                dots.append((i, j))
                sets.append(set())
        random.shuffle(dots)
        # print(dots)
        sets_num = 0
        for dot in dots:
            r = dot[0]
            c = dot[1]
            if self.v[r][c] == False:
                self.v[r][c] = True
                sets[sets_num].add((r, c))
                sets_num += 1

            d = random.randrange(0, 4)
            tmp = random.randrange(0, 2)
            dd = 1 if tmp == 1 else 3
            for i in range(4):
                rr = r + self.row[d]
                cc = c + self.col[d]
                if (rr >= 0 and rr < self.m) and (cc >= 0 and cc < self.n):
                    tmp = self.not_in_same_set(sets, (r,c), (rr, cc))
                    # print(tmp)
                    judge = tmp[0]
                    # print(judge)
                    set_num = tmp[1]

                    if judge == True:
                        continue
                    pop_item = -1
                    for i in range(sets_num):
                        if (rr, cc) in sets[i]:
                            pop_item = i
                            sets_num -= 1
                            break
                    # merge two set
                    if pop_item > -1:
                        sets[set_num] = sets[set_num] | sets[pop_item]
                        sets.pop(pop_item)
                    else:
                        sets[set_num].add((rr, cc))

                    self.v[rr][cc] = True
                    if d % 2 == 1:
                        self.R[r][c - (d == 1)] = True
                    else:
                        self.D[r - (d == 0)][c] = True
                d = (d + dd) % 4

    @staticmethod
    def not_in_same_set(sets, dot1, dot2):
        num = 0
        for i in sets:
            if dot1 in i:
                if dot2 in i:
                    return (True, num)
                else:
                    return (False, num)
            num += 1
        return (False, num)

    def print_console(self):
        for c in range(self.n):
            print("._", end="")
        print(".")
        for r in range(self.m):
            print("|", end="")
            for c in range(self.n):
                if self.D[r][c]:
                    print(" ", end="")
                else:
                    print("_", end="")
                if self.R[r][c]:
                    print(".", end="")
                else:
                    print("|", end="")
            print("")

if __name__ == '__main__':
    a = Maze(5, 5 ,50)
    # a.dfs_generate((20, 15))
    a.random_kruskal_generate()
    a.print_console()