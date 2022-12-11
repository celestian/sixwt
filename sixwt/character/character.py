# Copyright (C) 2022 sixwt Contributors, see LICENSE

import json
from enum import Enum, auto

try:
    from transitions.extensions import GraphMachine as FSMachine
except ImportError:
    from transitions import Machine as FSMachine

from transitions import Machine


class Priority(Enum):
    METATYPE = auto()
    ATTRIBUTES = auto()
    SKILLS = auto()
    MAGIC_RESONANCE = auto()
    RESOURCES = auto()


class States(Enum):
    INITIAL = auto()
    PRIORITY = auto()
    METATYPE = auto()


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
        self.__priorities = {
            "a": None,
            "b": None,
            "c": None,
            "d": None,
            "e": None,
        }
        FSMachine.__init__(self, states=States, send_event=True, initial=States.INITIAL)
        self.add_transition(
            trigger="add_priority",
            source=[States.INITIAL, States.PRIORITY],
            dest=States.PRIORITY,
            before="set_priority",
        )
        self.add_transition(
            trigger="add_metatype",
            source=States.PRIORITY,
            dest=States.METATYPE,
            before="set_metatype",
            conditions="are_priorities_set",
        )

    def __repr__(self):
        return json.dumps(self.get_data(), sort_keys=True, indent=2)

    def get_data(self):
        return {
            "name": self.__name,
            "priorities": self.__priorities,
        }

    def make_graph(self):
        if not isinstance(self.__class__, Machine):
            self.get_graph().draw("my_state_diagram.png", prog="dot")
        else:
            print("Library Graphviz is missing.")

    def set_priority(self, event):
        args = event.kwargs.get("args", {})
        priority = get_priority(args)
        value = get_priority_value(args)

        for i in ["a", "b", "c", "d", "e"]:
            if str(value) == self.__priorities[i]:
                raise ValueError(f"{value} was assigned before!")

        self.__priorities[priority] = str(value)

    def are_priorities_set(self, event):  # pylint: disable=unused-argument
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

    def set_metatype(self, event):  # pylint: disable=unused-argument
        # args = event.kwargs.get("args", {})
        return
