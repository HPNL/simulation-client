import requests
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Simulation, User

from dotenv import load_dotenv
import os

router = APIRouter(prefix="/api/v1", tags=["Simulations"])


# Pydantic models
class SimulationCreate(BaseModel):
    username: str
    simulation_data: str


class SimulationUpdate(BaseModel):
    status: str


@router.post("/simulations/create")
def create_simulation(simulation: SimulationCreate,
                      db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == simulation.username).first()

    db_simulation = Simulation(
        user_id=user.id,
        simulation_data=simulation.simulation_data
    )
    db.add(db_simulation)
    db.commit()
    db.refresh(db_simulation)
    return db_simulation


@router.get("/simulations/list/{username}")
def get_simulations_by_username(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()

    if user is None:
        return {"message": "کاربر یافت نشد"}

    db_simulations = db.query(Simulation).filter(Simulation.user_id == user.id).all()
    return db_simulations


@router.get("/simulations/{simulation_id}")
def get_simulation(simulation_id: int, db: Session = Depends(get_db)):
    db_simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if db_simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return db_simulation


@router.delete("/simulations/{simulation_id}")
def delete_simulation(simulation_id: int, db: Session = Depends(get_db)):
    db_simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()

    if db_simulation is None:
        raise HTTPException(status_code=404, detail="Simulation not found")

    db.delete(db_simulation)
    db.commit()

    return {"detail": "Simulation deleted successfully"}


@router.post("/simulation/run/{simulation_id}")
def run_simulation(simulation_id: int, db: Session = Depends(get_db)):
    load_dotenv()

    # خواندن مقادیر از فایل .env
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()

    # if simulation is None:
    #     raise HTTPException(status_code=404, detail="Simulation not found")
    #
    # if simulation.status != "NotStarted":
    #     raise HTTPException(status_code=400, detail="Simulation is already started or completed")

    simulation.status = "Running"
    db.commit()

    simulator_url = os.getenv("SIMULATOR.URL")
    response = requests.post(simulator_url, simulation.simulation_data)

    if response.status_code == 200:
        simulation.status = "Completed"
        db.commit()
        return {"message": "Simulation started and data sent successfully"}
    else:
        simulation.status = "Canceled"  # تغییر وضعیت به لغو شده
        db.commit()
        raise HTTPException(status_code=500, detail="Simulation failed to start")
