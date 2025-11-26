from __future__ import annotations

import threading
from enum import Enum, auto

import numpy as np
from fmpy import extract, read_model_description
from fmpy.fmi2 import FMU2Slave


class FMUState(Enum):
    CREATED = auto()
    INSTANTIATED = auto()
    INITIALIZATION_MODE = auto()
    INITIALIZED = auto()
    SIMULATION = auto()
    TERMINATED = auto()


class FMUSimulation:
    """
    FMUSimulation is a utility class that allows you to quickly run
    an FMU co-simulation in Python (via fmpy) designed to be used in notebooks.
    """

    def __init__(self, fmu_path: str):
        """
        Constructor. Loads and unzips the specified FMU file.
        Instantiates the FMI Slave (FMU2Slave) and sets its state to INSTANTIATED.
        """
        self.fmu_path = fmu_path

        self.unzip_dir = extract(fmu_path)
        self.model_description = read_model_description(fmu_path)
        self.experiment = self.model_description.defaultExperiment

        self.state = FMUState.CREATED
        self.lock = threading.Lock()

        self.fmu = FMU2Slave(
            guid=self.model_description.guid,
            unzipDirectory=self.unzip_dir,
            modelIdentifier=self.model_description.coSimulation.modelIdentifier,
            instanceName="instance",
        )

        with self.lock:
            self.fmu.instantiate()
            self.state = FMUState.INSTANTIATED

        self.vrs = {
            var.name: var.valueReference
            for var in self.model_description.modelVariables
        }

    def require_state(self, expected: FMUState, method: str):
        """
        Checks that the current FMU state (self.state) is the required expected state before a method can proceed.
        """
        if self.state != expected:
            msg = (
                f"{method}() requires FMU state {expected.name}, "
                f"but state is {self.state.name}"
            )
            raise RuntimeError(msg)

    def set(self, inputDic: dict):
        """
        Sets the values for FMU input variables or parameters.
        """
        for name, value in inputDic.items():
            if name not in self.vrs:
                msg = f"Variable '{name}' not found in FMU."
                raise KeyError(msg)

            vr = self.vrs[name]
            # var = self.model_description.get_variable(name)

            if isinstance(value, float):
                self.fmu.setReal([vr], [float(value)])
            elif isinstance(value, int):
                self.fmu.setInteger([vr], [int(value)])
            elif isinstance(value, bool):
                self.fmu.setBoolean([vr], [bool(value)])
            elif isinstance(value, str):
                self.fmu.setString([vr], [str(value)])
            else:
                msg = f"Unsupported variable type for '{name}'."
                raise TypeError(msg)

    def get(self, name):
        """
        Retrieves the Real value (as a float) of the specified output variable by name.
        """
        return self.fmu.getReal([self.vrs[name]])[0]

    def initialize(self, startTime=0.0, stopTime=3600.0, timeStep=1.0):
        """
        Prepares the FMU for simulation.
        Sets up the experiment (start time, stop time) and transitions the FMU to the INITIALIZATION_MODE state.
        """
        self.require_state(FMUState.INSTANTIATED, "initialize")

        self.start = startTime
        self.stop = stopTime
        self.step = timeStep

        with self.lock:
            self.fmu.setupExperiment(startTime=self.start, stopTime=self.stop)
            self.fmu.enterInitializationMode()
            self.state = FMUState.INITIALIZATION_MODE

    def exitInitialization(self):
        """
        Finalizes the FMU's initialization process.
        """

        self.require_state(FMUState.INITIALIZATION_MODE, "exitInitialization")

        with self.lock:
            self.fmu.exitInitializationMode()
            self.state = FMUState.INITIALIZED

    def initParameters(self, inputDic: dict):
        """
        Sets parameters during INITIALIZATION_MODE.
        Example: {'R': 10.5, 'G': 0.75}
        """
        self.require_state(FMUState.INITIALIZATION_MODE, "initParameters")

        with self.lock:
            self.set(inputDic)

    def updateInputs(self, inputDic: dict):
        """
        Update parameters during simulation.
        Example: {"InteriorHeatFlow.port.Q_flow": 20.0}
        """
        self.require_state(FMUState.SIMULATION, "updateInputs")

        with self.lock:
            self.set(inputDic)

    def run(self, outputs: list):
        """
        Executes the simulation step-by-step (doStep) from self.start to self.stop using a self.step size.
        """

        self.require_state(FMUState.INITIALIZED, "run")
        self.state = FMUState.SIMULATION

        time = self.start
        data = {name: [self.get(name)] for name in outputs}
        data["time"] = [time]
        for name in outputs:
            data[name] = []
            val = self.fmu.getReal([self.vrs[name]])[0]
            data[name].append(val)

        with self.lock:
            while time < self.stop:
                self.fmu.doStep(
                    currentCommunicationPoint=time, communicationStepSize=self.step
                )
                time += self.step
                data["time"].append(time)

                for name in outputs:
                    val = self.fmu.getReal([self.vrs[name]])[0]
                    data[name].append(val)
        return {key: np.array(value) for key, value in data.items()}

    def terminate(self):
        """
        Ends the simulation and releases the FMU resources.
        """
        if self.state == FMUState.TERMINATED:
            return

        with self.lock:
            self.fmu.terminate()
            self.state = FMUState.TERMINATED
