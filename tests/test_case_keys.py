import pytest
from env_var_doctor.env_var_doctor import EnvDoctor

def test_case_collisions(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("DATABASE_URL=postgres://localhost\ndatabase_url=mysql://localhost\n")
    ex_file = tmp_path / ".env.example"
    ex_file.write_text("DATABASE_URL=\n")
    
    doctor = EnvDoctor(env_path=str(env_file), example_path=str(ex_file))
    vars_map, errors = doctor.parse_env_file(str(env_file))
    # Verify behavior regarding case variants of variable names
    keys = list(vars_map.keys())
    assert "DATABASE_URL" in keys
    assert "database_url" in keys
