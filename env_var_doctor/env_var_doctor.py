import re
from typing import Dict, List, Tuple, Any, Optional

class EnvDoctor:
    def __init__(self, env_path: str = ".env", example_path: str = ".env.example"):
        self.env_path = env_path
        self.example_path = example_path

    def parse_env_string(self, content: str, source_name: str = "<string>") -> Tuple[Dict[str, str], List[str]]:
        vars_map: Dict[str, str] = {}
        errors: List[str] = []
        for line_no, line in enumerate(content.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped.startswith("\ufeff"):
                stripped = stripped.lstrip("\ufeff").strip()
            if re.match(r"^export\s+", stripped):
                stripped = re.sub(r"^export\s+", "", stripped)
            if "=" not in stripped:
                errors.append(f"{source_name}:{line_no}: Invalid syntax (missing '='): {stripped}")
                continue
            
            parts = stripped.split("=", 1)
            key = parts[0].strip()
            val = parts[1].strip()
            if "#" in val and not (val.startswith('"') and val.endswith('"')) and not (val.startswith("'") and val.endswith("'")):
                val = val.split("#", 1)[0].strip()
            
            if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
                errors.append(f"{source_name}:{line_no}: Invalid variable name: {key}")
                continue
                
            if key in vars_map:
                errors.append(f"{source_name}:{line_no}: Duplicate key detected: {key}")
            
            # Unquote values if quoted
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
                
            vars_map[key] = val
        return vars_map, errors

    def parse_env_file(self, filepath: str) -> Tuple[Dict[str, str], List[str]]:
        try:
            with open(filepath, "r", encoding="utf-8-sig") as f:
                content = f.read()
            return self.parse_env_string(content, filepath)
        except FileNotFoundError:
            return {}, []

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
