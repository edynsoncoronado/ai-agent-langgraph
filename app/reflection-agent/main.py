"""
Punto de entrada del agente de reflexión para LinkedIn.

Define un grafo de estado con LangGraph que alterna entre generar publicaciones
y reflexionar sobre ellas hasta alcanzar un resultado satisfactorio.
"""

# 1. IMPORTACIONES
#------------------------------------------------------------------------------------------------
# TypedDict define estructuras de datos tipadas; Annotated permite añadir metadatos
from typing import TypedDict, Annotated

# Reductor que fusiona listas de mensajes (añade en lugar de reemplazar)
from langgraph.graph.message import add_messages

# END indica fin del grafo; StateGraph construye el grafo de flujo
from langgraph.graph import END, StateGraph

# BaseMessage es la clase base para mensajes; HumanMessage representa mensajes del usuario
from langchain_core.messages import BaseMessage, HumanMessage

# Importamos las cadenas de generación y reflexión definidas en chains.py
from chains import generate_chain, reflect_chain


# 2. ESQUEMA DEL ESTADO DEL GRAFO
#------------------------------------------------------------------------------------------------
# Esquema del estado del grafo: un diccionario con clave "messages"
# Annotated con add_messages hace que los mensajes se acumulen en lugar de sustituirse
class MessageGraph(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# 3. CREACIÓN DE LOS NODOS DEL GRAFO
#------------------------------------------------------------------------------------------------
# Identificadores de los nodos del grafo
GENERATE = "generate"  # Nodo que genera o mejora la publicación
REFLECT = "reflect"   # Nodo que evalúa y critica la publicación


# Nodo de generación: invoca la cadena de generación con el historial actual
# y devuelve el estado actualizado con la nueva publicación generada
def generation_node(state: MessageGraph):
    # Invocamos la cadena de generación (prompt + LLM) con el historial
    generated_response = generate_chain.invoke({"messages": state["messages"]})

    # Devolvemos el estado actualizado; add_messages fusionará la respuesta al historial
    return {"messages": [generated_response]}


# Nodo de reflexión: invoca la cadena de reflexión que critica la publicación
# y devuelve la crítica como mensaje humano para que el siguiente ciclo la use
def reflection_node(state: MessageGraph):
    # Invocamos la cadena de reflexión con todo el historial
    res = reflect_chain.invoke({"messages": state["messages"]})
    # Envolvemos la respuesta en HumanMessage para que el modelo la interprete como feedback de humano
    return {"messages": [HumanMessage(content=res.content)]}


# 4. CONSTRUCCIÓN DEL GRAFO DE ESTADO
#------------------------------------------------------------------------------------------------
# Creamos el grafo de estado con el esquema MessageGraph
builder = StateGraph(state_schema=MessageGraph)

# Añadimos los nodos al grafo: GENERATE y REFLECT, con sus respectivas funciones
builder.add_node(GENERATE, generation_node)
builder.add_node(REFLECT, reflection_node)

# El grafo comienza en el nodo de generación
builder.set_entry_point(GENERATE)


# 5. CREACIÓN DE LAS ARISTAS DEL GRAFO
#------------------------------------------------------------------------------------------------
# Función de decisión para alternar entre generación y reflexión: siempre va de GENERATE a REFLECT
# El grafo se ejecutará en bucle entre estos dos nodos hasta que se alcance una condición de parada (ejemplo: máx. ~3 ciclos con 6 mensajes)
def should_continue(state: MessageGraph):
    # Si hay más de 6 mensajes en el historial, terminamos el grafo (evita bucles infinitos)
    if len(state["messages"]) > 6:
        return END
    # Si no, seguimos alternando entre generación y reflexión
    return REFLECT

# Arista condicional desde GENERATE: según la función should_continue, decide si ir a REFLECT o END, path_map define las aristas a seguir para visualizar correctamente el diagrama mermail
builder.add_conditional_edges(GENERATE, should_continue, path_map={REFLECT: REFLECT, END: END})

# Arista fija desde REFLECT a GENERATE: después de reflexionar, siempre volvemos a generar para mejorar la publicación
builder.add_edge(REFLECT, GENERATE)

# 6. COMPILACIÓN DEL GRAFO
#------------------------------------------------------------------------------------------------
# Compilamos el grafo para optimizar su ejecución
reflection_agent = builder.compile()

# Mostrar el grafo en formato Mermaid para visualizar su estructura
print(reflection_agent.get_graph().draw_mermaid()) # Puedes visualizar el diagrama Mermaid en https://mermaidviewer.com/editor o cualquier editor compatible con Mermaid
# reflection_agent.get_graph().print_ascii()  # También puedes mostrarlo en formato ASCII en la consola


# 7. EJECUCIÓN DEL AGENTE DE REFLEXIÓN
#------------------------------------------------------------------------------------------------
# Ejecutamos el agente de reflexión, al ejecutar el script directamente (python main.py) se iniciará el proceso iterativo de generación y reflexión
if __name__ == "__main__":
    print("Hola LangGraph")

    # Entrada de ejemplo: un mensaje humano pidiendo mejorar una publicación
    initial_input = HumanMessage(content="Ayúdame a escribir una publicación de LinkedIn sobre inteligencia artificial.")
    inputs = {"messages": [initial_input]}  # El estado inicial del grafo con el mensaje del usuario

    # Invocamos el agente de reflexión con la entrada inicial y obtenemos el resultado final después de las iteraciones de generación y reflexión
    response = reflection_agent.invoke(inputs)

    # Mostramos la respuesta final (estado con el historial completo de mensajes, incluyendo la publicación final generada y las críticas)
    for m in response["messages"]:
        print(type(m).__name__, ":", m.content)