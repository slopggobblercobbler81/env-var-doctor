import pytest
from env_var_doctor.env_var_doctor import EnvDoctor


def test_parse_env_string_direct():
    doctor = EnvDoctor()
    content = """
    APP_ENV=staging
    DATABASE_PORT=5432
    """
    vars_map, errors = doctor.parse_env_string(content)
    assert errors == []
    assert vars_map["APP_ENV"] == "staging"
    assert vars_map["DATABASE_PORT"] == "5432"


def test_utf8_bom_handling(tmp_path):
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"

    # Write file starting with UTF-8 BOM
    content_with_bom = "\ufeffSERVICE_NAME=order-service\nPORT=8080\n"
    env_file.write_text(content_with_bom, encoding="utf-8")
    example_file.write_text("SERVICE_NAME=\nPORT=\n", encoding="utf-8")

    doctor = EnvDoctor(str(env_file), str(example_file))
    res = doctor.check_variables()
    assert res["errors"] == []
    assert "SERVICE_NAME" in res["env_vars"]
    assert res["env_vars"]["SERVICE_NAME"] == "order-service"
