import re
from typing import Dict, List, Tuple, Any, Optional

class EnvDoctor:
    def __init__(self, env_path: str = ".env", example_path: str = ".env.example"):
        self.env_path = env_path
        self.example_path = example_path

    def parse_env_file(self, filepath: str) -> Tuple[Dict[str, str], List[str]]:
        vars_map: Dict[str, str] = {}
        errors: List[str] = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    stripped = line.strip()
                    if not stripped or stripped.startswith("#"):
                        continue
                    if "=" not in stripped:
                        errors.append(f"{filepath}:{line_no}: Invalid syntax (missing '='): {stripped}")
                        continue
                    
                    parts = stripped.split("=", 1)
                    key = parts[0].strip()
                    val = parts[1].strip()
                    
                    if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
                        errors.append(f"{filepath}:{line_no}: Invalid variable name: {key}")
                        continue
                        
                    if key in vars_map:
                        errors.append(f"{filepath}:{line_no}: Duplicate key detected: {key}")
                    
                    # Unquote values if quoted
                    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                        val = val[1:-1]
                        
                    vars_map[key] = val
        except FileNotFoundError:
            pass
        return vars_map, errors

    def check_variables(self) -> Dict[str, Any]:
        env_vars, env_errors = self.parse_env_file(self.env_path)
        ex_vars, ex_errors = self.parse_env_file(self.example_path)

        all_errors = env_errors + ex_errors
        missing_vars = [k for k in ex_vars if k not in env_vars]
        extra_vars = [k for k in env_vars if k not in ex_vars]

        return {
            "env_vars": env_vars,
            "ex_vars": ex_vars,
            "missing_vars": missing_vars,
            "extra_vars": extra_vars,
            "errors": all_errors
        }
