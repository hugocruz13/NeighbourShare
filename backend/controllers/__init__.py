from .recurso_controller import router as recurso_controller
from .reserva_controller import router as reserva_controller
from .recurso_comum_controller import router as recurso_comum_controller
from .notificacao_controller import router as notificacao_controller

routers = [recurso_controller, reserva_controller, recurso_comum_controller, notificacao_controller]