from typing import List
from simulation.airless_earth_ambient import AirlessEarthAmbient
from simulation.earth_ambient import EarthAmbient
from core.physics.body.rigid_body import RigidBody
from core.physics.forces.translation_test_force import TranslationTestForce
from core.physics.forces.rotation_test_force import RotationTestForce
from core.physics.vector import Vector
from core.physics.body.application_point import ApplicationPoint
from models.structure.rocket_model import RocketModel

from rb_test.trajectory_test import trajectoryTest
from rb_test.velocity_test import velocityTest
from rb_test.angular_velocity_test import angularVelocityTest

from core.physics.forces.weight_force import WeightForce
from rb_test.acceleration_test import accelerationTest
from models.structure.nose_model import NoseModel
from models.structure.nose_model import NoseType
from models.structure.transition_model import TransitionModel
from models.other.material_model import MaterialModel
from models.structure.cylindrical_body_model import CylindricalBodyModel
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from utils.utils import Utils
from models.structure.fin_model import FinModel
from models.structure.rocket_model import RocketParts


# def isOnLine(line: List[Vector], point: Vector):
#     a = (line[1].y() - line[0].y()) / (line[1].x() - line[0].x())
#     b = line[0].y() - a * line[0].x()
#     y = a * line[0].x() + b
#     y = float(str(f"{y:.4f}"))
#
#     y_point = float(str(f"{point.y():.4f}"))
#
#     return y == y_point


def geometryTest():
    fig = plt.figure(figsize=(8, 5))
    # ax = fig.add_subplot(111, projection='3d')
    ax = fig.gca(projection='3d')
    print()
    parts = rocket.getParts()
    for part in parts:
        delimitation_points = part.delimitation_points
        coords = [part.part_type]

        for delimitation in delimitation_points:
            coords.append(delimitation.toList())

        print(coords)
        print(f"    {part.part_type} cg: {part.cg}")
        print(f"    {part.part_type} cp: {part.cp}")

        ax.scatter(delimitation_points[0].x(), delimitation_points[0].y(), delimitation_points[0].z(), color="red")
        ax.scatter(delimitation_points[1].x(), delimitation_points[1].y(), delimitation_points[1].z(), color="red")
        ax.scatter(part.cg.x(), part.cg.y(), part.cg.z(), color="green")
        ax.scatter(part.cp.x(), part.cp.y(), part.cp.z(), color="lightgreen")

    print()
    print(f"Rocket CG: {rocket.cg}")
    print(f"Rocket CP: {rocket.cp}")

    # plt.show()


def physicsTest():
    weight = WeightForce()
    thrust_test = TranslationTestForce(130, 0, 600)
    # trajectoryTest(rocket, [weight, thrust_test], 100, arrow_scale=400, has_arrows=True)
    trajectoryTest(rocket, [weight, thrust_test], 100, arrow_scale=400, has_arrows=True)


acrylic = MaterialModel("acrylic")
nose = NoseModel(2, 0.5, NoseType.PARABOLIC, 1, 0.2, acrylic, 0) 
# transition = TransitionModel(0.5, 2, 2, 0.5, acrylic, 1)
cylinder1 = CylindricalBodyModel(5, 2, 0.5, acrylic, 2)  # height 5
# cylinder2 = CylindricalBodyModel(4, 2, 0.5, acrylic, 3)  # height 4 , rocket_height = 10
fins = FinModel(1, 0.5, 1.5, 0.05, 0.3925, 0, 2, 4, acrylic, 4)

rocket = RocketModel()
rocket.addPart(nose)
rocket.addPart(cylinder1)
rocket.addPart(fins)
rotation = Vector(0, 0.1, 0)
rocket.rotate(rotation)

# ambient = EarthAmbient()
ambient = AirlessEarthAmbient()
trajectoryTest(rocket, ambient, 10, arrow_scale=1, has_arrows=True, limit=20, additional_forces=[], step=0.2, debug=False)

# rocket.rotate(rotation)

# physicsTest()
# geometryTest()

# [<RocketParts.NOSE: 'nose'>, [0.0, 0.0, 6.0], [0.0, 0.0, 5.0]]
#     RocketParts.NOSE cg: (0.0, 0.0, 5.333333333333333)
#     RocketParts.NOSE cp: (0.0, 0.0, 5.5)
# [<RocketParts.CYLINDRICAL_BODY: 'cylidrical body'>, [0.0, 0.0, 5.0], [0.0, 0.0, 0.0]]
#     RocketParts.CYLINDRICAL_BODY cg: (0.0, 0.0, 2.5)
#     RocketParts.CYLINDRICAL_BODY cp: (0.0, 0.0, 2.5)

# Rocket CG: (0.0, 0.0, 2.8331842193272525)
# Rocket CP: (0.0, 0.0, 5.5)
