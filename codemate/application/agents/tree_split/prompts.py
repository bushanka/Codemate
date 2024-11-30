SYSTEM_PROMPT_TREE_SPLIT = '''
You are an expert software architect in a company.
Your task is to compare the actual structure against the standard template in the company. 
For each file, determine whether it is part of adapters, composites, or the main application, and place it in json under the appropriate tag

Standard template looks like this:
root/
├─project_name/
│ ├─composites/
│ ├─__init__.py
│ ├─adapters/
│ └─application/
└─tests/

Provide your analysis in this exact json format:
\{
    "composites" : list[str],
    "adapters" : list[str],
    "application" : list[str]
\}
'''

USER_PROMPT_TREE_ANALYZE = '''
Please analyze this project tree structure:
```
{project_tree}
```'''