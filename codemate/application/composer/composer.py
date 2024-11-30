from agents.code_analyzer import CodeAnalyzerAgent
from agents.tree_analyzer import TreeAnalyzerAgent
from agents.tree_split import TreeSplitAgent

import json
import ast
import astor

class Composer():
    """Должен брать всех агентов в нужной последовательности в зависимости от типа: 1 файл или zip (проект)
    и execut'ить их код, получать отчеты, сохранять и потом составлять финальный отчет агентом для финального отчета
    """
    def __init__(self):
        self._code_analyser = CodeAnalyzerAgent()
        self._tree_analyser = TreeAnalyzerAgent()
        self._tree_split = TreeSplitAgent()
    
    # analyze architecture
    def create_report_for_project(self, project_dir: str) ->str:
        final_report = ""

        # get overall architecture prediction
        overall_code_analyze = self._tree_analyser.create_report(project_path=project_dir).to_text()
        
        # find every possible code files to check
        final_report += overall_code_analyze + "\n"
        list_of_files_in_json_str = self._tree_split.create_report(project_path=project_dir).to_text()
        try:
            list_of_files = json.loads(list_of_files_in_json_str)  # Convert JSON string to dictionary
        except ValueError as e:
            list_of_files = None  # Or handle the error appropriately
        
        # for every found file analyze its content on architecture standart
        if list_of_files is not None:
            for layer in list_of_files.keys():
                for filepath in list_of_files['layer']:
                    response = self.create_report_for_file(filepath, layer)
                    final_report += response + "\n"

        return final_report
    
    def create_report_for_file(self, filepath, layer=""):
        final_report = ""
        code_snippets = self._get_functions_and_classes(filepath)
        for c_s in code_snippets:  
            if layer != "":
                architecture_code_analyzer_response = self._code_analyser.create_report(
                    file_path=filepath, 
                    layer_name=layer, 
                    code_content=c_s
                    ).to_text()
                if architecture_code_analyzer_response != "":
                    final_report += architecture_code_analyzer_response + "\n"
            else:
                NotImplemented
                # добавим агентов, которые проверяет код на предмет плохо-написанного мусора
        return final_report
                

    def _get_functions_and_classes(self, file_path):
        with open(file_path, 'r') as file:
            file_content = file.read()

        tree = ast.parse(file_content)
        
        functions_and_classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions_and_classes.append(astor.to_source(node))
            elif isinstance(node, ast.ClassDef):
                functions_and_classes.append(astor.to_source(node))
        
        return functions_and_classes
