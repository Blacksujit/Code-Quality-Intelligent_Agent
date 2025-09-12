"""
Advanced AST Parsing for Code Structure Analysis
Provides deep code structure analysis using Abstract Syntax Trees
"""

import ast
from typing import Dict, List, Tuple, Set, Optional
from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict, Counter


@dataclass
class CodeStructure:
    """Represents code structure analysis results"""
    file_path: str
    language: str
    functions: List[Dict]
    classes: List[Dict]
    imports: List[Dict]
    complexity_metrics: Dict
    design_patterns: List[Dict]
    code_smells: List[Dict]
    dependencies: List[Dict]


class ASTAnalyzer:
    """Advanced AST-based code structure analyzer"""
    
    def __init__(self):
        self.design_patterns = {
            'singleton': self._detect_singleton,
            'factory': self._detect_factory,
            'observer': self._detect_observer,
            'decorator': self._detect_decorator,
            'strategy': self._detect_strategy,
            'builder': self._detect_builder
        }
        
        self.code_smells = {
            'long_method': self._detect_long_method,
            'large_class': self._detect_large_class,
            'duplicate_code': self._detect_duplicate_code,
            'dead_code': self._detect_dead_code,
            'complex_conditional': self._detect_complex_conditional,
            'magic_numbers': self._detect_magic_numbers,
            'deep_nesting': self._detect_deep_nesting
        }
    
    def analyze_file(self, file_path: str, content: str, language: str) -> CodeStructure:
        """Analyze a single file for code structure"""
        if language == 'python':
            return self._analyze_python_file(file_path, content)
        elif language in ['javascript', 'typescript']:
            return self._analyze_js_file(file_path, content)
        else:
            return self._analyze_generic_file(file_path, content, language)
    
    def _analyze_python_file(self, file_path: str, content: str) -> CodeStructure:
        """Analyze Python file using AST"""
        try:
            tree = ast.parse(content)
        except SyntaxError:
            return self._create_empty_structure(file_path, 'python')
        
        functions = []
        classes = []
        imports = []
        complexity_metrics = {}
        design_patterns = []
        code_smells = []
        dependencies = []
        
        # Analyze AST nodes
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = self._analyze_function(node, content)
                functions.append(func_info)
                
                # Check for code smells
                smells = self._check_function_smells(node, content)
                code_smells.extend(smells)
            
            elif isinstance(node, ast.ClassDef):
                class_info = self._analyze_class(node, content)
                classes.append(class_info)
                
                # Check for code smells
                smells = self._check_class_smells(node, content)
                code_smells.extend(smells)
            
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                import_info = self._analyze_import(node)
                imports.append(import_info)
                dependencies.append(import_info)
        
        # Calculate complexity metrics
        complexity_metrics = self._calculate_complexity_metrics(tree, content)
        
        # Detect design patterns
        design_patterns = self._detect_design_patterns(tree, content)
        
        return CodeStructure(
            file_path=file_path,
            language='python',
            functions=functions,
            classes=classes,
            imports=imports,
            complexity_metrics=complexity_metrics,
            design_patterns=design_patterns,
            code_smells=code_smells,
            dependencies=dependencies
        )
    
    def _analyze_function(self, node: ast.FunctionDef, content: str) -> Dict:
        """Analyze a function definition"""
        lines = content.split('\n')
        start_line = node.lineno
        end_line = node.end_lineno or start_line
        
        # Calculate metrics
        lines_of_code = end_line - start_line + 1
        parameters = len(node.args.args)
        local_vars = len([n for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)])
        
        # Calculate cyclomatic complexity
        complexity = self._calculate_cyclomatic_complexity(node)
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        # Extract decorators
        decorators = [ast.unparse(dec) for dec in node.decorator_list]
        
        return {
            'name': node.name,
            'start_line': start_line,
            'end_line': end_line,
            'lines_of_code': lines_of_code,
            'parameters': parameters,
            'local_variables': local_vars,
            'cyclomatic_complexity': complexity,
            'docstring': docstring,
            'decorators': decorators,
            'is_async': isinstance(node, ast.AsyncFunctionDef),
            'is_generator': any(isinstance(n, ast.Yield) for n in ast.walk(node)),
            'content': '\n'.join(lines[start_line-1:end_line])
        }
    
    def _analyze_class(self, node: ast.ClassDef, content: str) -> Dict:
        """Analyze a class definition"""
        lines = content.split('\n')
        start_line = node.lineno
        end_line = node.end_lineno or start_line
        
        # Extract methods
        methods = []
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                method_info = self._analyze_function(item, content)
                method_info['is_method'] = True
                methods.append(method_info)
        
        # Calculate metrics
        lines_of_code = end_line - start_line + 1
        method_count = len(methods)
        attribute_count = len([n for n in node.body if isinstance(n, ast.Assign)])
        
        # Extract docstring
        docstring = ast.get_docstring(node)
        
        # Extract base classes
        base_classes = [ast.unparse(base) for base in node.bases]
        
        return {
            'name': node.name,
            'start_line': start_line,
            'end_line': end_line,
            'lines_of_code': lines_of_code,
            'method_count': method_count,
            'attribute_count': attribute_count,
            'methods': methods,
            'base_classes': base_classes,
            'docstring': docstring,
            'content': '\n'.join(lines[start_line-1:end_line])
        }
    
    def _analyze_import(self, node: ast.Import) -> Dict:
        """Analyze an import statement"""
        if isinstance(node, ast.Import):
            return {
                'type': 'import',
                'module': node.names[0].name,
                'alias': node.names[0].asname,
                'line': node.lineno
            }
        elif isinstance(node, ast.ImportFrom):
            return {
                'type': 'from_import',
                'module': node.module,
                'names': [name.name for name in node.names],
                'aliases': [name.asname for name in node.names],
                'line': node.lineno
            }
    
    def _calculate_cyclomatic_complexity(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor)):
                complexity += 1
            elif isinstance(child, ast.ExceptHandler):
                complexity += 1
            elif isinstance(child, (ast.And, ast.Or)):
                complexity += 1
        
        return complexity
    
    def _calculate_complexity_metrics(self, tree: ast.AST, content: str) -> Dict:
        """Calculate various complexity metrics"""
        lines = content.split('\n')
        
        # Basic metrics
        total_lines = len(lines)
        code_lines = len([line for line in lines if line.strip() and not line.strip().startswith('#')])
        comment_lines = len([line for line in lines if line.strip().startswith('#')])
        blank_lines = len([line for line in lines if not line.strip()])
        
        # Function and class counts
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        # Calculate average complexity
        total_complexity = sum(self._calculate_cyclomatic_complexity(f) for f in functions)
        avg_complexity = total_complexity / len(functions) if functions else 0
        
        # Calculate nesting depth
        max_nesting = self._calculate_max_nesting_depth(tree)
        
        return {
            'total_lines': total_lines,
            'code_lines': code_lines,
            'comment_lines': comment_lines,
            'blank_lines': blank_lines,
            'function_count': len(functions),
            'class_count': len(classes),
            'total_complexity': total_complexity,
            'average_complexity': avg_complexity,
            'max_nesting_depth': max_nesting,
            'comment_ratio': comment_lines / code_lines if code_lines > 0 else 0
        }
    
    def _calculate_max_nesting_depth(self, node: ast.AST, current_depth: int = 0) -> int:
        """Calculate maximum nesting depth"""
        max_depth = current_depth
        
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.AsyncFor, ast.With, ast.AsyncWith)):
                depth = self._calculate_max_nesting_depth(child, current_depth + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = self._calculate_max_nesting_depth(child, current_depth)
                max_depth = max(max_depth, depth)
        
        return max_depth
    
    def _detect_design_patterns(self, tree: ast.AST, content: str) -> List[Dict]:
        """Detect design patterns in the code"""
        patterns = []
        
        for pattern_name, detector in self.design_patterns.items():
            if detector(tree, content):
                patterns.append({
                    'name': pattern_name,
                    'confidence': 0.8,  # Simplified confidence scoring
                    'description': self._get_pattern_description(pattern_name)
                })
        
        return patterns
    
    def _detect_singleton(self, tree: ast.AST, content: str) -> bool:
        """Detect Singleton pattern"""
        # Look for classes with __new__ method and instance variable
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                has_new = any(isinstance(item, ast.FunctionDef) and item.name == '__new__' 
                             for item in node.body)
                has_instance = '_instance' in content or 'instance' in content
                if has_new and has_instance:
                    return True
        return False
    
    def _detect_factory(self, tree: ast.AST, content: str) -> bool:
        """Detect Factory pattern"""
        # Look for functions that create and return objects
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if 'create' in node.name.lower() or 'make' in node.name.lower():
                    # Check if function returns an object
                    for child in ast.walk(node):
                        if isinstance(child, ast.Return) and isinstance(child.value, ast.Call):
                            return True
        return False
    
    def _detect_observer(self, tree: ast.AST, content: str) -> bool:
        """Detect Observer pattern"""
        # Look for subscribe/notify methods
        subscribe_methods = any('subscribe' in content.lower() or 'attach' in content.lower())
        notify_methods = any('notify' in content.lower() or 'update' in content.lower())
        return subscribe_methods and notify_methods
    
    def _detect_decorator(self, tree: ast.AST, content: str) -> bool:
        """Detect Decorator pattern"""
        # Look for functions that take functions as parameters and return functions
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check if function takes another function as parameter
                has_func_param = any(isinstance(arg.annotation, ast.Name) and 
                                   'Callable' in ast.unparse(arg.annotation)
                                   for arg in node.args.args)
                if has_func_param:
                    return True
        return False
    
    def _detect_strategy(self, tree: ast.AST, content: str) -> bool:
        """Detect Strategy pattern"""
        # Look for classes with similar methods but different implementations
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        if len(classes) < 2:
            return False
        
        # Check if classes have similar method signatures
        method_signatures = defaultdict(list)
        for cls in classes:
            for method in cls.body:
                if isinstance(method, ast.FunctionDef):
                    sig = (method.name, len(method.args.args))
                    method_signatures[sig].append(cls.name)
        
        # Check for common method signatures across classes
        for sig, class_names in method_signatures.items():
            if len(class_names) > 1:
                return True
        
        return False
    
    def _detect_builder(self, tree: ast.AST, content: str) -> bool:
        """Detect Builder pattern"""
        # Look for classes with many optional parameters and builder methods
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if 'builder' in node.name.lower():
                    return True
                # Check for methods that return self (method chaining)
                for method in node.body:
                    if isinstance(method, ast.FunctionDef):
                        for stmt in method.body:
                            if isinstance(stmt, ast.Return) and isinstance(stmt.value, ast.Name) and stmt.value.id == 'self':
                                return True
        return False
    
    def _check_function_smells(self, node: ast.FunctionDef, content: str) -> List[Dict]:
        """Check for code smells in functions"""
        smells = []
        
        # Long method
        if self._detect_long_method(node, content):
            smells.append({
                'type': 'long_method',
                'severity': 'medium',
                'description': f'Function {node.name} is too long ({node.end_lineno - node.lineno + 1} lines)',
                'line': node.lineno
            })
        
        # Complex conditional
        if self._detect_complex_conditional(node, content):
            smells.append({
                'type': 'complex_conditional',
                'severity': 'medium',
                'description': f'Function {node.name} has complex conditional logic',
                'line': node.lineno
            })
        
        # Deep nesting
        if self._detect_deep_nesting(node, content):
            smells.append({
                'type': 'deep_nesting',
                'severity': 'high',
                'description': f'Function {node.name} has deep nesting levels',
                'line': node.lineno
            })
        
        return smells
    
    def _check_class_smells(self, node: ast.ClassDef, content: str) -> List[Dict]:
        """Check for code smells in classes"""
        smells = []
        
        # Large class
        if self._detect_large_class(node, content):
            smells.append({
                'type': 'large_class',
                'severity': 'medium',
                'description': f'Class {node.name} is too large ({node.end_lineno - node.lineno + 1} lines)',
                'line': node.lineno
            })
        
        return smells
    
    def _detect_long_method(self, node: ast.FunctionDef, content: str) -> bool:
        """Detect if method is too long"""
        return (node.end_lineno or node.lineno) - node.lineno > 50
    
    def _detect_large_class(self, node: ast.ClassDef, content: str) -> bool:
        """Detect if class is too large"""
        return (node.end_lineno or node.lineno) - node.lineno > 200
    
    def _detect_duplicate_code(self, node: ast.AST, content: str) -> bool:
        """Detect duplicate code (simplified)"""
        # This is a simplified implementation
        # In practice, you'd use more sophisticated algorithms
        return False
    
    def _detect_dead_code(self, node: ast.AST, content: str) -> bool:
        """Detect dead code (simplified)"""
        # This is a simplified implementation
        return False
    
    def _detect_complex_conditional(self, node: ast.FunctionDef, content: str) -> bool:
        """Detect complex conditional logic"""
        complexity = self._calculate_cyclomatic_complexity(node)
        return complexity > 10
    
    def _detect_magic_numbers(self, node: ast.AST, content: str) -> bool:
        """Detect magic numbers"""
        # Look for numeric literals that aren't 0, 1, or common values
        magic_numbers = []
        for child in ast.walk(node):
            if isinstance(child, ast.Constant) and isinstance(child.value, (int, float)):
                if child.value not in [0, 1, 2, 10, 100, 1000]:
                    magic_numbers.append(child.value)
        return len(magic_numbers) > 3
    
    def _detect_deep_nesting(self, node: ast.FunctionDef, content: str) -> bool:
        """Detect deep nesting"""
        max_depth = self._calculate_max_nesting_depth(node)
        return max_depth > 4
    
    def _get_pattern_description(self, pattern_name: str) -> str:
        """Get description for design pattern"""
        descriptions = {
            'singleton': 'Ensures a class has only one instance',
            'factory': 'Creates objects without specifying their exact class',
            'observer': 'Defines a one-to-many dependency between objects',
            'decorator': 'Adds behavior to objects dynamically',
            'strategy': 'Defines a family of algorithms and makes them interchangeable',
            'builder': 'Constructs complex objects step by step'
        }
        return descriptions.get(pattern_name, 'Unknown pattern')
    
    def _analyze_js_file(self, file_path: str, content: str) -> CodeStructure:
        """Analyze JavaScript/TypeScript file (simplified)"""
        # This is a simplified implementation
        # In practice, you'd use a JavaScript parser like esprima
        return self._create_empty_structure(file_path, 'javascript')
    
    def _analyze_generic_file(self, file_path: str, content: str, language: str) -> CodeStructure:
        """Analyze generic file"""
        return self._create_empty_structure(file_path, language)
    
    def _create_empty_structure(self, file_path: str, language: str) -> CodeStructure:
        """Create empty structure for unsupported languages"""
        return CodeStructure(
            file_path=file_path,
            language=language,
            functions=[],
            classes=[],
            imports=[],
            complexity_metrics={},
            design_patterns=[],
            code_smells=[],
            dependencies=[]
        )


def analyze_code_structure(file_path: str, content: str, language: str) -> CodeStructure:
    """Main function to analyze code structure"""
    analyzer = ASTAnalyzer()
    return analyzer.analyze_file(file_path, content, language)
