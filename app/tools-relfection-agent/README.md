Este código implementa un **agente reflexivo (Reflection Agent)** con LangGraph. La idea es:

1. Generar una respuesta inicial (_draft_).
2. Ejecutar herramientas para buscar información adicional.
3. Revisar y mejorar la respuesta.
4. Decidir si necesita seguir investigando o terminar.

# Diagrama de alto nivel
```
┌─────────────┐
│   START     │
└──────┬──────┘
       │
       ▼
┌───────────────────┐
│     BORRADOR      │
│   draft_node()    │
│                   │
│ first_responder   │
│ genera respuesta  │
│ inicial           │
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│ EXECUTE_TOOLS     │
│ execute_tools()   │
│                   │
│ Ejecuta búsquedas │
│ y herramientas    │
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│     REVISOR       │
│   revise_node()   │
│                   │
│ revisor analiza   │
│ resultados y      │
│ mejora respuesta  │
└──────┬────────────┘
       │
       ▼
┌───────────────────┐
│   event_loop()    │
│                   │
│ ¿Se alcanzó el    │
│ máximo de vueltas?│
└───┬─────────┬─────┘
    │ Sí      │ No
    ▼         ▼
 ┌──────┐  ┌───────────────┐
 │ END  │  │ EXECUTE_TOOLS │
 └──────┘  └───────────────┘
````

# Grafo construído
``` mermaid
flowchart TD

START --> Borrador

Borrador --> ExecuteTools

ExecuteTools --> Revisor

Revisor --> Decision

Decision -->|Continuar| ExecuteTools

Decision -->|Finalizar| END
```

# Arquitectura interna
``` mermaid
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        borrador(borrador)
        execute_tools(execute_tools)
        revisor(revisor)
        __end__([<p>__end__</p>]):::last
        __start__ --> borrador;
        borrador --> execute_tools;
        execute_tools --> revisor;
        revisor -.-> __end__;
        revisor -.-> execute_tools;
```


# Patrón de diseño utilizado

Este código implementa el patrón:

```
Generate
    ↓
Critique
    ↓
Search
    ↓
Revise
    ↓
Repeat
```

o, formalmente:

```
Reflexion Agent
(Self-Reflection Agent)
```

muy parecido al paper:
[Reflexion: Language Agents with Verbal Reinforcement Learning ](https://openreview.net/pdf?id=vAElhFcKW6)

donde un modelo:
1. Produce una respuesta.
2. Evalúa sus propias deficiencias.
3. Obtiene nueva información.
4. Reescribe la respuesta.
5. Repite hasta alcanzar un criterio de parada.

