from .recurso_controller import router as recurso_controller
from .reserva_controller import router as reserva_controller
from.recurso_comum_controller import router as recurso_comum_controller

routers = [recurso_controller, reserva_controller, recurso_comum_controller]