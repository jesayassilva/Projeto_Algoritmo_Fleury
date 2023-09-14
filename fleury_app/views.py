from django.shortcuts import render
from .models import *
# Create your views here.
import copy


def index(request):
    erro = ''
    try:
        msg = False
        resultado=''
        if  request.method == "POST":
            msg = True
            grafo = request.POST.get("grafo")
            grafo = eval(grafo)
            fleury = Fleury(grafo)
            resultado = fleury.run()
        else:
            visitantes = Visitantes()
            visitantes.save()
    except Exception as e:
        erro = str(e)
    return render(request,'index.html',{'msg':msg,'resultado':resultado,'erro':erro,'visitantes':Visitantes.objects.all().count()})





class FleuryException(Exception):
    def __init__(self, message):
        super(FleuryException, self).__init__(message)
        self.message = message

class Fleury:
    COLOR_WHITE = 'white'
    COLOR_GRAY = 'gray'
    COLOR_BLACK = 'black'

    def __init__(self, graph):

        self.graph = graph

    def run(self):
        menssagem = 'Aplicando o algoritmo Fleury para o grafo: \n\n'
        for v in self.graph:
            menssagem = menssagem + str(v) + ' => '+ str(self.graph[v])+'\n'
        menssagem = menssagem + '\n'
        output = None
        try:
            output = self.fleury(self.graph)
        except FleuryException as message:
            menssagem = menssagem + str(message)
            return menssagem
        if output:
            menssagem = menssagem + 'Encontrado Ciclo Euleriano.\n\n'
            for v in output:
                menssagem = menssagem + str(v) + '\n'
        #print (menssagem)
        return menssagem

    def is_connected(self, G):
        start_node = list(G)[0]
        color = {}
        iterator = 0;
        for v in G:
            color[v] = Fleury.COLOR_WHITE
        color[start_node] = Fleury.COLOR_GRAY
        S = [start_node]
        while len(S) != 0:
            u = S.pop()
            for v in G[u]:
                if color[v] == Fleury.COLOR_WHITE:
                    color[v] = Fleury.COLOR_GRAY
                    S.append(v)
                color[u] = Fleury.COLOR_BLACK
        return list(color.values()).count(Fleury.COLOR_BLACK) == len(G)

    def even_degree_nodes(self, G):
        even_degree_nodes = []
        for u in G:
            if len(G[u]) % 2 == 0:
                even_degree_nodes.append(u)
        return even_degree_nodes

    def is_eulerian(self, even_degree_odes, graph_len):
        return graph_len - len(even_degree_odes) == 0

    def convert_graph(self, G):
        links = []
        for u in G:
            for v in G[u]:
                links.append((u, v))
        return links

    def fleury(self, G):
        edn = self.even_degree_nodes(G)
        if not self.is_eulerian(edn, len(G)):
            raise FleuryException('O grafo fornecido não é um grafo de Euler')
        g = copy.copy(G)
        cycle = []
        # wybieramy dowolny wierzchołek w grafie o niezerowym stopniu
        u = edn[0]
        while len(self.convert_graph(g)) > 0:
            current_vertex = u
            for u in list(g[current_vertex]): # OSOBNA KOPIA
                g[current_vertex].remove(u)
                g[u].remove(current_vertex)

                bridge = not self.is_connected(g)
                if bridge:
                    g[current_vertex].append(u)
                    g[u].append(current_vertex)
                else:
                    break
            if bridge:
                g[current_vertex].remove(u)
                g[u].remove(current_vertex)
                g.pop(current_vertex)
            cycle.append((current_vertex, u))
        return cycle
