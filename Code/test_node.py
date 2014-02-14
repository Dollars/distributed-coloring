from node import Node

def main():
    nodes = [Node() for i in range(22)]

    for i, n in enumerate(nodes):
        n.add(*nodes[i+1:i+4])

    for n in nodes:
        print(n)

    no = Node(*nodes)
    print(no)

if __name__ == "__main__":
    main()