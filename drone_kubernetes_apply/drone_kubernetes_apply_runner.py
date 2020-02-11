from drone_kubernetes_apply.functions.envvars.envvars import *
from drone_kubernetes_apply.functions.file.file import *
from parse_it import ParseIt
import os


def init():
    # read envvars
    print("reading envvars")
    parser = ParseIt(recurse=False, envvar_prefix="plugin_", config_type_priority=["env_vars"])
    parser.read_configuration_variable("kubernetes_token", required=True)
    parser.read_configuration_variable("kuberentes_api_host", required=True)
    kubernetes_file = parser.read_configuration_variable("kubernetes_yaml_file",
                                                         default_value="injected_deployment.yaml")
    kubernetes_file = os.getcwd() + "/" + kubernetes_file
    envvar_dict = read_all_envvars_to_dict()

    # get the job json
    print("reading kubernetes YAML file")
    kubernetes_file_yaml = read_file(kubernetes_file)

    # populate the job json with the template data
    print("populating kubernetes YAML file with the templated data")
    kubernetes_file_yaml = populate_template_string(kubernetes_file_yaml, envvar_dict)

    # TODO - create the modified file
