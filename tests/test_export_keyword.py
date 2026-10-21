import pytest
from env_var_doctor.env_var_doctor import EnvDoctor


def test_export_keyword_parsing(tmp_path):
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"

    env_content = """# Export prefix test
export FOO=bar
export   PORT=3000
export DATABASE_URL="postgres://user:pass@localhost:5432/app"
NORMAL_VAR=active
"""
    example_content = """FOO=
PORT=
DATABASE_URL=
NORMAL_VAR=
"""

    env_file.write_text(env_content)
    example_file.write_text(example_content)

    doctor = EnvDoctor(str(env_file), str(example_file))
    res = doctor.check_variables()

    assert len(res["errors"]) == 0
    assert len(res["missing_vars"]) == 0
    assert res["env_vars"]["FOO"] == "bar"
    assert res["env_vars"]["PORT"] == "3000"
    assert res["env_vars"]["DATABASE_URL"] == "postgres://user:pass@localhost:5432/app"
    assert res["env_vars"]["NORMAL_VAR"] == "active"
