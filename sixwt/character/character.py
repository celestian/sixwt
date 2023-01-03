# Copyright (C) 2022 sixwt Contributors, see LICENSE

import json
from enum import Enum, auto

try:
    from transitions.extensions import GraphMachine as FSMachine
except ImportError:
    from transitions import Machine as FSMachine

from transitions import Machine


class BuildSystem(Enum):
    PT_PRIORITY_TABLE = auto()
    SUM_TO_TEN = auto()
    POINT_BUY = auto()
    LIFE_PATH = auto()


class Priority(Enum):
    METATYPE = auto()
    ATTRIBUTES = auto()
    SKILLS = auto()
    MAGIC_RESONANCE = auto()
    RESOURCES = auto()


class States(Enum):
    INITIAL = auto()
    BS_PT_PRIORITY_TABLE = auto()
    BS_SUM_TO_TEN = auto()
    BS_POINT_BUY = auto()
    BS_LIFE_PATH = auto()
    PT_PRIORITY = auto()
    PT_METATYPE = auto()


def get_priority(args):
    priority = None
    for i in ["a", "b", "c", "d", "e"]:
        if args[i]:
            priority = i
            break
    return priority


def get_priority_value(args):
    if args["metatype"]:
        return Priority.METATYPE
    if args["attributes"]:
        return Priority.ATTRIBUTES
    if args["skills"]:
        return Priority.SKILLS
    if args["magic_resonance"]:
        return Priority.MAGIC_RESONANCE
    if args["resources"]:
        return Priority.RESOURCES

    return None


class Character(FSMachine):
    def __init__(self, name):
        self.__name = " ".join(name)
        self.__build_system = None
        self.__priorities = {
            "a": None,
            "b": None,
            "c": None,
            "d": None,
            "e": None,
        }
        FSMachine.__init__(self, states=States, send_event=True, initial=States.INITIAL)

        # INITIAL --> BS_PT_PRIORITY_TABLE
        self.add_transition(
            trigger="add_bs_priority_table",
            source=States.INITIAL,
            dest=States.BS_PT_PRIORITY_TABLE,
            before="set_bs_priority_table",
        )

        # INITIAL --> BS_SUM_TO_TEN
        self.add_transition(
            trigger="add_bs_sum_to_ten",
            source=States.INITIAL,
            dest=States.BS_SUM_TO_TEN,
            before="set_bs_sum_to_ten",
        )

        # INITIAL --> BS_POINT_BUY
        self.add_transition(
            trigger="add_bs_point_buy",
            source=States.INITIAL,
            dest=States.BS_POINT_BUY,
            before="set_bs_point_buy",
        )

        # INITIAL --> BS_LIFE_PATH
        self.add_transition(
            trigger="add_bs_life_path",
            source=States.INITIAL,
            dest=States.BS_LIFE_PATH,
            before="set_bs_life_path",
        )

        # ------------------------

        # BS_PT_PRIORITY_TABLE, PT_PRIORITY --> PT_PRIORITY
        self.add_transition(
            trigger="add_pt_priority",
            source=[States.INITIAL, States.PT_PRIORITY],
            dest=States.PT_PRIORITY,
            before="set_pt_priority",
        )

        # PT_PRIORITY --> PT_METATYPE
        self.add_transition(
            trigger="add_pt_metatype",
            source=States.PT_PRIORITY,
            dest=States.PT_METATYPE,
            before="set_pt_metatype",
            conditions="are_pt_priorities_set",
        )

    def __repr__(self):
        return json.dumps(self.get_data(), sort_keys=True, indent=2)

    def get_data(self):
        return {
            "name": self.__name,
            "priorities": self.__priorities,
            "build_system": self.__build_system,
        }

    def make_graph(self):
        if not isinstance(self.__class__, Machine):
            self.get_graph().draw("my_state_diagram.png", prog="dot")
        else:
            print("Library Graphviz is missing.")

    def set_bs_priority_table(self, event):  # pylint: disable=unused-argument
        self.__build_system = BuildSystem.PT_PRIORITY_TABLE

    def set_bs_sum_to_ten(self, event):  # pylint: disable=unused-argument
        self.__build_system = BuildSystem.SUM_TO_TEN

    def set_bs_point_buy(self, event):  # pylint: disable=unused-argument
        self.__build_system = BuildSystem.POINT_BUY

    def set_bs_life_path(self, event):  # pylint: disable=unused-argument
        self.__build_system = BuildSystem.LIFE_PATH

    def set_pt_priority(self, event):
        args = event.kwargs.get("args", {})
        priority = get_priority(args)
        value = get_priority_value(args)

        for i in ["a", "b", "c", "d", "e"]:
            if str(value) == self.__priorities[i]:
                raise ValueError(f"{value} was assigned before!")

        self.__priorities[priority] = str(value)

    def are_pt_priorities_set(self, event):  # pylint: disable=unused-argument
        is_ready = True
        used = []
        for i in ["a", "b", "c", "d", "e"]:
            if not self.__priorities[i]:
                is_ready = False

            if self.__priorities[i] not in used:
                used.append(self.__priorities[i])
            else:
                is_ready = False
        return is_ready

    def set_pt_metatype(self, event):  # pylint: disable=unused-argument
        # args = event.kwargs.get("args", {})
        return
