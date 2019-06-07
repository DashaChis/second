import urllib.request
import matplotlib.pyplot as plt
import gensim
import networkx as nx
from networkx.algorithms import community
from os.path import join
from flask import Flask, render_template, request


def find_similar(key_word): 
    get_gen = get_m()
    if key_word in get_gen:
        fin = []
        for i in get_gen.most_similar(positive=[key_word], topn=8):
            fin.append((str(i[0]), i[1]))
        return fin
        
def get_m():
    '''urllib.request.urlretrieve(
        "http://rusvectores.org/static/models/rusvectores2/ruscorpora_mystem_cbow_300_2_2015.bin.gz",
        "ruscorpora_mystem_cbow_300_2_2015.bin.gz")'''
    response = 'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
    get_gen = gensim.models.KeyedVectors.load_word2vec_format(response, binary=True)
    return get_gen

def draw(key_word, fin):
    Gr = nx.Graph()
    Gr.add_node(key_word)
    for f in fin:
        Gr.add_node(f[0], label=f[0])
        Gr.add_edge(key_word, f[0], weight=f[2])
        fin_al = find_similar(f[0])
        for a in fin_al:
            Gr.add_node(a[0], label=a[0])
            Gr.add_edge(f[0], a[0], weight=a[2])
   # print('узлы', Gr.nodes())
   # print('рёбра', Gr.edges())
    return Gr

def measure(Gr):  
    rad = nx.radius(Gr)
    dia = nx.diameter(Gr)
    pearson = nx.degree_pearson_correlation_coefficient(Gr)
   # print(nx.degree_pearson_correlation_coefficient(Gr))
    dens = nx.density(Gr)
   # print(nx.density(Gr))
    return rad, dia, pearson, dens

def graaph(Gr, key_word): 
    pos = nx.spring_layout(Gr)
    nx.draw_networkx_edges(Gr, pos, edge_color='green')
    nx.draw_networkx_nodes(Gr, pos, node_color='yellow', node_size=40)
    nx.draw_networkx_labels(Gr, pos, font_size=6, font_family='Calibri')
    plt.axis('off') 
    plt.show()
    pth = join('static', 'graph.png')
    plt.savefig(pth, dpi=400)
    plt.clf()

def knots(Gr):  
    centr = nx.degree_centrality(Gr)
    degcen = [nodeid for nodeid in sorted(centr, key=centr.get, reverse=True)]
    centr = nx.closeness_centrality(Gr)
    clocen = [nodeid for nodeid in sorted(centr, key=centr.get, reverse=True)]
    centr = nx.betweenness_centrality(Gr)
    betcen = [nodeid for nodeid in sorted(centr, key=centr.get, reverse=True)]
    centr = nx.eigenvector_centrality(Gr)
    eigcen = [nodeid for nodeid in sorted(centr, key=centr.get, reverse=True)]
    return degcen, clocen, betcen, eigcen


app = Flask(__name__)

@app.route('/')
def index():
    if request.args:
        bul = str(request.args['key_word'])
        try:
            Gr = draw(bul, find_similar(bul))
            graaph(Gr, bul)
            file_name = bul + '.png'
            rad, dia = measure(Gr)
            degcen, clocen, betcen, eigcen = knots(Gr)
            return render_template('results.html', rad=rad, dia=dia, dens=dens, pearson=pearson, degcen=degcen[:4], clocen=clocen[:4], betcen=betcen[:4], eigcen=eigcen[:4])
        except IndexError:
            print('oy')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=False)
