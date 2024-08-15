from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List


app = FastAPI()

class RideRequest(BaseModel):
    origem: str
    destino: str
    distancia: float

class Ride(BaseModel):
    id: int
    origem: str
    destino: str
    distancia: float
    valor: float
    status: str = "Requisitada"

rides: List[Ride] = []
next_id = 1

@app.post("/rides", response_model=Ride, status_code=201)
def Criar_Corrida(ride_request: RideRequest):
    global next_id
    ride = Ride(
        id =next_id,
        origem = ride_request.origem,
        destino = ride_request.destino,
        distancia = ride_request.distancia,
        valor = 6.65 + 2 * ride_request.distancia,
    )
    rides.append(ride)    
    next_id +=1
    return ride

@app.get("/rides/{ride_id}", response_model=List[Ride])
def Listar_Corrida(status: str = None):
    if status:
        return [ride for ride in rides if ride.status.lower() == status.lower()]
    return rides

@app.put("/rides/{ride_id}" , response_model = Ride)
def Atualizar_Corrida(ride_id: int, ride_request: RideRequest):
    ride = next((r for r in rides if r.id == ride_id), None)
    if not ride or ride.status not in [ "Requisitada", "Em Andamento"]:
        raise HTTPException(status_code=404, detail="Corrida não encontrada ou em não estado válido !") # type: ignore
    ride.origem = ride_request.origem
    ride.destino = ride_request.destino
    ride.distancia = ride_request.distancia
    ride.valor = 6.65 + 2 * ride_request.distancia
    return ride

@app.post("/rides/{ride_id}/finish", response_model = Ride)
def Finalizar_Corrida(ride_id: int):
    ride = next((r for r in rides if r.id == ride_id),None)
    if not ride or ride.status != "Em Andamento":
        raise HTTPException(status_code=404, detail="Corrida não encontrada ou em não estado válido !") # type: ignore
    ride.status = "Finalizado"
    return ride

@app.delete("/rides/{ride_id}", status_code = 204)
def Deletar_Corrida(ride_id: int):
    ride = next((r for r in rides if r.id == ride_id), None)
    if not ride or ride.status != "Requisitada":
        raise HTTPException(status_code=404, detail="Corrida não encontrada ou em não estado válido !") # type: ignore
    rides.remove(ride)
