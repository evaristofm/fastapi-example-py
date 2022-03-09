from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse
from urllib3 import Retry

from api_pedidos.esquemas import Item
from api_pedidos.excecao import PedidoNaoEncontradoError, FalhaDeComunicacaoError

app = FastAPI()

@app.exception_handler(PedidoNaoEncontradoError)
def tratar_erro_pedido_nao_encontrado(request: Request, exc: PedidoNaoEncontradoError):
    return JSONResponse(status_code=HTTPStatus.NOT_FOUND, content={"message": "Pedido não encontrado"})

@app.exception_handler(FalhaDeComunicacaoError)
def tratar_erro_falha_de_comunicacao(request: Request, exc: FalhaDeComunicacaoError):
    return JSONResponse(status_code=HTTPStatus.BAD_GATEWAY, content={"message": "Falha de comunicação com o servidor remoto"})


def recuperar_itens_por_pedido(identificacao_do_pedido: UUID) -> List[Item]:
    pass


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}

@app.get("/orders/{identificacao_do_pedido}/items")
def listar_itens(itens: List[Item] = Depends(recuperar_itens_por_pedido)):
    return itens
