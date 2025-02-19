from ophyd import Component as Cpt
from ophyd import EpicsMotor, EpicsSignal
from ophyd.epics_motor import MotorBundle

from dodal.devices.motors import MotorLimitHelper, XYZLimitBundle


class Smargon(MotorBundle):
    """
    Real motors added to allow stops following pin load (e.g. real_x1.stop() )
    X1 and X2 real motors provide compound chi motion as well as the compound X travel,
    increasing the gap between x1 and x2 changes chi, moving together changes virtual x.
    Robot loading can nudge these and lead to errors.
    """

    x: EpicsMotor = Cpt(EpicsMotor, "X")
    y: EpicsMotor = Cpt(EpicsMotor, "Y")
    z: EpicsMotor = Cpt(EpicsMotor, "Z")
    chi: EpicsMotor = Cpt(EpicsMotor, "CHI")
    phi: EpicsMotor = Cpt(EpicsMotor, "PHI")
    omega: EpicsMotor = Cpt(EpicsMotor, "OMEGA")

    stub_offset_set: EpicsSignal = Cpt(EpicsSignal, "SET_STUBS_TO_RL.PROC")
    """Stub offsets are calibration values that are required to move between calibration
    pin position and spine pins. These are set in EPICS and applied via the proc."""

    real_x1: EpicsMotor = Cpt(EpicsMotor, "MOTOR_3")
    real_x2: EpicsMotor = Cpt(EpicsMotor, "MOTOR_4")
    real_y: EpicsMotor = Cpt(EpicsMotor, "MOTOR_1")
    real_z: EpicsMotor = Cpt(EpicsMotor, "MOTOR_2")
    real_phi: EpicsMotor = Cpt(EpicsMotor, "MOTOR_5")
    real_chi: EpicsMotor = Cpt(EpicsMotor, "MOTOR_6")

    def get_xyz_limits(self) -> XYZLimitBundle:
        """Get the limits for the x, y and z axes.

        Note that these limits may not yet be valid until wait_for_connection is called
        on this MotorBundle.

        Returns:
            XYZLimitBundle: The limits for the underlying motors.
        """
        return XYZLimitBundle(
            MotorLimitHelper(self.x),
            MotorLimitHelper(self.y),
            MotorLimitHelper(self.z),
        )
