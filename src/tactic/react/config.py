
__all__ = ["ConfigCmd", "BaseElementWdg", "BaseEditElementWdg"]

import os
import json

from pyasm.common import Common
from pyasm.command import Command


class ConfigCmd(Command):

    # overrie this metho
    def get_config(self):
        return {}


    def get_full_config(self):
        self.execute()
        return self.info.get("config")




    def execute(self):
        config = self.get_config().copy()
        config = self.process_config(config)

        edit_handlers = {}
        for item in config:
            name = item.get("name")

            edit = item.get("edit")
            if not edit:
                edit = "tactic.react.BaseEditElementWdg"
            kwargs = {
                "config": item,
            }
            handler = Common.create_from_class_path(edit, [], kwargs)
            handler.preprocess()

            edit_handlers[name] = handler



        # preprocess all of the handlers
        """
        display_handlers = {}
        for item in config:
            name = item.get("name")

            display = item.get("display")
            if not display:
                display = "tactic.react.BaseElementWdg"
            kwargs = {
                "config": item,
                "sobjects": sobjects
            }
            handler = Common.create_from_class_path(display, [], kwargs)
            handler.preprocess()

            display_handlers[name] = handler
        """


        self.info["config"] = config


    def process_config(self, config):

        for item in config:

            item_type = item.get("type")
            if item_type == "select":

                values = item.get("values")
                labels = item.get("labels")

                values_expr = item.get("values_expr")
                if values_expr:
                    values = Search.eval(values_expr)

                item["values"] = values

                labels_expr = item.get("labels_expr")
                if labels_expr:
                    labels = Search.eval(labels_expr)

                item["labels"] = labels

        return config



class BaseElementWdg():

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.sobjects = kwargs.get("sobjects")
        self.config = kwargs.get("config")
        self.sobject = None


    def set_current_sobject(self, sobject):
        self.sobject = sobject

    def get_current_sobject(self):
        return self.sobject

    def get_sobjects(self):
        return self.sobjects

    def preprocess(self):
        return

    def execute(self, data):
        return


class BaseEditElementWdg():

    def __init__(self, **kwargs):
        self.kwargs = kwargs

        self.config = kwargs.get("config")
        self.sobject = None


    def preprocess(self):
        pass

