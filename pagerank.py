import re
import codecs
import random
import linecache


class Pagerank(object):
    def __init__(self, links_file, pages_file):
        self.links_file = links_file
        self.pages_file = pages_file
        self.jump = 15
        self.limit = 1
        self.edge = sum(1 for line in open(links_file))
        self.vertex = sum(1 for line in open(pages_file))
        self.adjacency_list = {}
        self.visited = [0]*self.vertex

    def read(self):
        with open(self.links_file, "r") as f:
            for line in f:
                items = line[:-1].split()
                if items[0] in self.adjacency_list:
                    self.adjacency_list[items[0]].append(items[1])
                else:
                    self.adjacency_list[items[0]] = [items[1]]

    def surf(self):
        current = random.choice(list(self.adjacency_list.keys()))
        for i in range(self.limit):
            if (random.randint(0, 99) < self.jump) \
                    or (current not in self.adjacency_list.keys()):
                current = random.choice(list(self.adjacency_list.keys()))
            self.visited[int(current)] += 1
            current = random.choice(self.adjacency_list[current])

    def rank(self, parcent):
        if not re.compile("^\d+(\.\d+)?\Z").match(parcent):
            raise Exception("無効な入力値です。0~100の数値を入力してください")
        if float(parcent) < 0 or 100 < float(parcent):
            raise Exception("無効な数値です。0~100の数値を入力してください")

        print("全体の{}%以上のスコアを獲得したページは".format(parcent))
        for index, visited in enumerate(self.visited):
            if visited >= self.limit*float(parcent)/100:
                print(linecache.getline(self.pages_file, index+1), end="")

    def output(self):
        with codecs.open("dest.txt", "w", "utf-8") as f:
            for index, times in enumerate(self.visited):
                f.write("%s %s\n" % (index, times))


if __name__ == '__main__':
    pagerank = Pagerank("wikipedia_links/small_links.txt",
                        "wikipedia_links/small_pages.txt")
    pagerank.read()
    pagerank.surf()
    pagerank.output()
    while True:
        pagerank.rank(input("ページランクスコア何%以上？ --> "))
