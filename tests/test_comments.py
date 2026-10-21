import os
import pytest
from env_var_doctor.env_var_doctor import EnvDoctor

def test_missing_vars(tmp_path):
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"
    env_file.write_text("PORT=8080\n")
    example_file.write_text("PORT=8080\nDATABASE_URL=postgres://...\n")

    doctor = EnvDoctor(str(env_file), str(example_file))
    res = doctor.check_variables()
    assert "DATABASE_URL" in res["missing_vars"]

def test_syntax_error(tmp_path):
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"
    env_file.write_text("INVALID_SYNTAX_LINE\n")
    example_file.write_text("PORT=8080\n")

    doctor = EnvDoctor(str(env_file), str(example_file))
    res = doctor.check_variables()
    assert len(res["errors"]) > 0

def test_duplicate_key(tmp_path):
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"
    env_file.write_text("PORT=8080\nPORT=9090\n")
    example_file.write_text("PORT=8080\n")

    doctor = EnvDoctor(str(env_file), str(example_file))
    res = doctor.check_variables()
    assert any("Duplicate key" in err for err in res["errors"])

def test_inline_comments(tmp_path):
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"
    env_file.write_text("PORT=8080 # This is a port comment\nHOST=localhost # host comment\n")
    example_file.write_text("PORT=8080\nHOST=localhost\n")

    doctor = EnvDoctor(str(env_file), str(example_file))
    res = doctor.check_variables()
    assert res["env_vars"]["PORT"] == "8080"
    assert res["env_vars"]["HOST"] == "localhost"
