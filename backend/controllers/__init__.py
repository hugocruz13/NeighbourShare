from .recurso_controller import router as recurso_controller
from .reserva_controller import router as reserva_controller
from .recurso_comum_controller import router as recurso_comum_controller
from .orcamento_controller import router as orcamento_controller
from .auth_controller import router as auth_controller

routers = [recurso_controller, reserva_controller, recurso_comum_controller, orcamento_controller, auth_controller]