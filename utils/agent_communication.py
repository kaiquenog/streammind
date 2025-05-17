from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

def call_agent(agent: Agent, message_text: str) -> str:
    """Funu00e7u00e3o para chamar um agente e obter sua resposta"""
    session_service = InMemorySessionService()
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    print(f"\nDEBUG: Enviando para o agente '{agent.name}': '{message_text}'")
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        # Tenta imprimir o tipo de evento se o atributo event_type existir
        if hasattr(event, 'event_type'):
            print(f"DEBUG: Evento recebido: Tipo='{event.event_type}'")
        else:
            # Se event_type nu00e3o existir, imprime os atributos disponu00edveis para ajudar na depurau00e7u00e3o
            print(f"DEBUG: Evento recebido (atributos: {dir(event)})")

        if event.content and event.content.parts:
            for i, part in enumerate(event.content.parts):
                print(f"DEBUG: Evento Part[{i}]:")
                if part.text is not None:
                    print(f"  DEBUG: Part.text: '{part.text}'")

                # Logging para chamadas de funu00e7u00e3o (comum com Gemini e google-adk)
                if hasattr(part, 'function_call') and part.function_call:
                    print(f"  DEBUG: Part.function_call: Name='{part.function_call.name}', Args='{part.function_call.args}'")

                # Logging para respostas de funu00e7u00e3o/ferramenta
                if hasattr(part, 'function_response') and part.function_response:
                    print(f"  DEBUG: Part.function_response: Name='{part.function_response.name}', Response='{part.function_response.response}'")

                # Logging mais genu00e9rico para tool_code e tool_response, caso function_call nu00e3o seja o u00fanico
                if hasattr(part, 'tool_code') and part.tool_code and not (hasattr(part, 'function_call') and part.function_call) : # Evitar duplicidade se function_call ju00e1 foi logado
                    print(f"  DEBUG: Part.tool_code: Name='{part.tool_code.name}', Args='{part.tool_code.args}'")
                if hasattr(part, 'tool_response') and part.tool_response and not (hasattr(part, 'function_response') and part.function_response): # Evitar duplicidade
                    print(f"  DEBUG: Part.tool_response: Name='{part.tool_response.name}', Content='{part.tool_response.content}'")


        if event.is_final_response():
          print("DEBUG: Evento u00e9 resposta final.")
          if event.content and event.content.parts:
              for part in event.content.parts:
                if part.text is not None:
                  final_response += part.text
                  final_response += "\n"
    print(f"DEBUG: Resposta final bruta do agente '{agent.name}':\n{final_response.strip()}")
    return final_response.strip()
