from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify, redirect, request
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError
from schemas.event import EventSchema, EventBuscaSchema, ListagemEventsSchema, EventDelSchema, EventViewSchema
from services.event import EventService
import pudb

info = Info(title="Micro Appointment API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags definitions
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
event_tag = Tag(name="Event", description="Adição, visualização, atualização e remoção de events à base (testado)")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect('/openapi')

@app.get('/hello', tags=[home_tag])
def hello():
    """Retorna um simples HTML com a mensagem Hello World."""
    return """
    <html>
        <head>
            <title>Hello World</title>
        </head>
        <body>
            <h1>Hello World</h1>
        </body>
    </html>
    """

@app.get('/hello-world', tags=[home_tag])
def hello_world():
    """Retorna um simples hello world."""
    print('testessssssss', flush=True)
    return jsonify({"message": "Hello World"})

#///////////////////////////////////////////////////////////////////////////////////////
# APPOINTMENTS
#///////////////////////////////////////////////////////////////////////////////////////

#POST
@app.post('/appointment', tags=[event_tag],
          responses={"200": EventViewSchema, "409": {"description": "Erro de duplicidade"}, "400": {"description": "Erro de requisição"}})
def add_event(body: EventSchema):
    """Adiciona um novo Event à base de dados.
    
    Retorna uma representação dos events e comentários associados.
    """
    return EventService.add_event(body)

#GET ALL
@app.get('/appointments', tags=[event_tag],
         responses={"200": ListagemEventsSchema, "404": {"description": "Event não encontrado"}})
def get_events():
    """Faz a busca por todos os Event cadastrados.
    
    Retorna uma representação da listagem de events. Se o parâmetro "user_id" for
    fornecido na query string, somente os events desse usuário serão retornados.
    """
    return EventService.get_events()
#GET ONE
@app.get('/appointment', tags=[event_tag],
         responses={"200": EventViewSchema, "404": {"description": "Event não encontrado"}})
def get_event(query: EventBuscaSchema):
    """Faz a busca por um Event a partir do name do event.
    
    Retorna uma representação dos events e comentários associados.
    """
    return EventService.get_event(query)

#DELETE
@app.delete('/appointment', tags=[event_tag],
            responses={"200": EventDelSchema, "404": {"description": "Event não encontrado"}})
def del_event(query: EventBuscaSchema):
    """Deleta um Event a partir do name do event informado.
    
    Retorna uma mensagem de confirmação da remoção.
    """
    return EventService.del_event_by_id_and_user(query)

@app.put('/appointment', tags=[event_tag],
         responses={"200": EventViewSchema, "404": {"description": "Event não encontrado"}, "400": {"description": "Erro de requisição"}})
def update_event(query: EventBuscaSchema, body: EventSchema):
    """
    Atualiza um Event utilizando os parâmetros de query (id e user_id) e os dados enviados no body.
    
    Retorna uma representação do event atualizado.
    """
    return EventService.update_event(query, body)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
