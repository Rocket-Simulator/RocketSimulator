from core.recovery.maximum_force import maximum_force
from typing import List
from core.physics.vector import Vector
from utils.rocket_parts import RocketParts
from utils.cable_type import CableType
from utils.parachute_type import ParachuteType
from utils.paths import Paths
from core.physics.body.rigid_body import RigidBody
from models.other.material_model import MaterialModel
from math import pi
from models.structure.abstract_model import AbstractModel
import json
import enum
from random import randint


class EjectionCriteria(enum.Enum):
    APOGEE = 1

class ParachuteModel(AbstractModel):
    def __init__(self, ejection_criteria:EjectionCriteria, parachute_type: ParachuteType, cable_type:CableType, diameter:float, coupled_part:AbstractModel, inflation_randomness_factor: float = 1):
        self.ejection_criteria = ejection_criteria
        self.height = 0
        self.parachute_type = parachute_type
        self.inflation_randomness_factor = inflation_randomness_factor
        self.cable_type = cable_type
        self.diameter = diameter
        self.coupled_part = coupled_part
        self.ejected = False
        self.inflated = False
        self.inflation_force = None
        self.drag_coefficient = self.__calculateDragCoefficient()
        self.transversal_area = self.__calculateTransversalArea()

        super().__init__(RocketParts.PARACHUTE, coupled_part.position_order, 1_000_000, self.drag_coefficient, self.transversal_area)
        self.__verify(diameter)

    def __verify(self, diameter:float): # fazer
        """Verifica se os campos indicados pelo usuário são possíveis (incompleto).

            Raises:
                ValueError: Algum campo é incoerente.
        """
        pass

    def eject(self): # concertar para ajustar o fator randomico de acordo com DELTA_TIME
        if self.inflated is True:
            return

        self.ejected = True
        upper_limit = int(2**(self.inflation_randomness_factor * 2))
        inflation_tentative = randint(1, upper_limit)
        if inflation_tentative == 1: # success
            print("inflated")
            self.inflated = True
            self.calculateMaximumInflationForce()
    
    def calculateMaximumInflationForce(self):
        pass
        # self.inflation_force = maximum_force(parachute_drag_force:float, opening_shock:float)

    def __calculateDragCoefficient(self):
        """Calcula o coeficiente de arrasto.

        Returns:
            (float): Coeficiente de arrasto.
        """
        drag_coefficient = None
        parachute_folder = Paths.PARACHUTES.value

        parachute_file = f"{parachute_folder}/{self.parachute_type.value}.json"
        with open(parachute_file) as parachute_file:
            data = json.load(parachute_file)

            drag_coefficient = data["drag_coefficient"]

        return drag_coefficient

    def __calculateTransversalArea(self) -> float:
        """Calcula a área transversal no instante T-0.

        Returns:
            (float): Área transversal.
        """
        return ((self.diameter/2)**2)*5.099

    def calculateMass(self):
        return 0

    def calculateMomentOfInertia(self, distance_to_cg:float):
        return 0

    def calculateVolume(self):
        return 0

    def calculateWetArea(self):
        return self.__calculateTransversalArea()

    # def calculateVolume(self) -> float: # possivelmente errado
    #     inner_diameter = self.diameter - 2 * self.thickness
    #     volume = pi * self.height * ((self.diameter / 2) ^ 2 - (inner_diameter / 2) ^ 2)
    #     return volume

    # def calculateMass(self) -> float: # possivelmente errado
    #     mass = self.material.density * self.calculateVolume
    #     return mass

    # def calculateMomentOfInertia(self, distance_to_cg: float) -> float: # possivelmente errado
    #     mass = self.calculateMass
    #     Ixx = 1/12*mass*(3*( (self.diameter^2)/4 +((self.diameter-2*self.thickness)^2)/4 )+self.height^2)
    #     return Ixx

    def calculateCg(self) -> Vector: # possivelmente errado
        return self.toGroundCoordinates(Vector(0, 0, 0))

    def calculateCp(self) -> Vector: # possivelmente errado
        return self.toGroundCoordinates(Vector(0, 0, 0))

    def createDelimitationPoints(self) -> List[Vector]: # possivelmente errado
        return [Vector(0, 0, 0), Vector(0, 0, 0)]

    
