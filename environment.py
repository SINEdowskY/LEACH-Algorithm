import networkx as nx
import matplotlib as plt
import random
import math

class Environment:

    def __init__(self, nodes_amount: int) -> None:
        self.nodes_amount = nodes_amount
        self.graph = nx.Graph() #Graph
        self.nodes: list = [] #nodes
        self.random_positions: list = [] #random positions
        self.nodes_positions: dict #positions assigned to nodes
        self.antenna_node = 'antenna' # antenna node
        self.antenna_node_position = [self.nodes_amount/2, self.nodes_amount] # antenna position
        self.nodes_color: list = []

        self.cluster_heads: dict = {}

        self.__generate_nodes()
        self.__generate_positions()
        self.__add_nodes_to_graph()
        self.__generate_random_cluster_heads()
        self.update_cluster_heades()
        self.create_node_colors()
        self.edges_to_antenna()
        self.clustering()

    def __generate_nodes(self):
        """
        Generate nodes
        """
        for i in [x for x in range(self.nodes_amount)]:
            self.nodes.append(f"node_{i}")
    
    def __generate_positions(self):
        """
        generate positions for nodes
        """
        amount_iterated = list(range(self.nodes_amount))
        for i in [x for x in amount_iterated]:
            random_x = random.randint(0, self.nodes_amount)
            random_y = random.randint(0, self.nodes_amount-10)
            pair = [random_x, random_y]
            if pair not in amount_iterated:
                self.random_positions.append([random_x, random_y])
            else:
                amount_iterated.append(amount_iterated[-1]+1)
               
        

    def __add_nodes_to_graph(self):
        """
        Add all nodes in graph
        """
        for i, node in enumerate(self.nodes):
            rand_energy = random.randint(10, 200)
            self.graph.add_node(node, name=node, pos=self.random_positions[i], energy=rand_energy, is_ch=False, is_taken = False, is_dead=False, color="green")
        
        self.graph.add_node(self.antenna_node, name='antenna', pos=self.antenna_node_position, energy=None, is_ch=None, is_taken = None, is_dead=None, color="blue")
        self.nodes_positions = nx.get_node_attributes(self.graph, 'pos')

    def __generate_random_cluster_heads(self):
        """
        generate dict of c
        """
        ifwas = []
        for i in range(7):
            rand = random.randint(0, self.nodes_amount)
            if not(rand in ifwas):
                self.cluster_heads[f'node_{rand}'] = {
                    "is_ch": True,
                    "color": "red"
                }
                ifwas.append(rand)
    
    def update_cluster_heades(self):
        nx.set_node_attributes(self.graph, self.cluster_heads)

    def create_node_colors(self):
        for color in self.graph.nodes(data="color"):
            self.nodes_color.append(color[1])

    
    def edges_to_antenna(self):
        """
        Add edges to antenna
        """
        ch_length_to_antenna = [['antenna', 0.0]]
        graph_nodes_data = self.graph.nodes.items()
        for node, nodedata in graph_nodes_data:
            if nodedata['is_ch'] == True:
                length = (nodedata['pos'][0] - self.antenna_node_position[0])**2 + (nodedata['pos'][1] - self.antenna_node_position[1])**2
                ch_length_to_antenna.append([node, math.sqrt(length)])
        
        ch_length_to_antenna = sorted(ch_length_to_antenna, key=lambda l:l[1])

        for i in range(1, len(ch_length_to_antenna)):
            self.graph.add_edge(ch_length_to_antenna[i-1][0], ch_length_to_antenna[i][0])
    
    def clustering(self):
        graph_nodes_data = self.graph.nodes.items()
        distances_to_chs = dict()
        for node_ch, nodedata_ch in graph_nodes_data:
            if nodedata_ch['is_ch']:
                distances_to_chs[node_ch] = {}
                for node, nodedata in graph_nodes_data:
                    if nodedata['is_ch'] == False:
                        length = (nodedata['pos'][0] - nodedata_ch['pos'][0])**2 + (nodedata['pos'][1] - nodedata_ch['pos'][1])**2
                        distances_to_chs[node_ch][node] = {'length': length, 'is taken': False}
        

        res = {key : dict(sorted(val.items(), key = lambda ele: ele[1].get("length",0), reverse=False))
               for key, val in distances_to_chs.items()}
        #print(res)

        print(res)
        for el in res.items():
            print(el)
        #for ch in res:
        #    data = iter(res[ch])
        #    i = 0
        #    nodes = []
        #    for el in data:
        #        if i != 3:
        #            nodes.append(el)
        #            i += 1
        #        else:
        #            break
        #
        #    for node in nodes:
        #        self.graph.add_edge(ch, node, color='red')

    def draw_graph(self):
         return nx.draw(self.graph, font_size=10, pos=self.nodes_positions, node_size=30, node_color=self.nodes_color)


    



        
        

    #def draw_graph(self):