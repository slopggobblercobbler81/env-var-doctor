import time
import pytest
from env_var_doctor.env_var_doctor import EnvDoctor

def test_benchmark_parsing_throughput(tmp_path):
    """Verify throughput parsing of 1,000+ environment variable lines with edge cases."""
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"

    lines = []
    # Generate 1,200 distinct environment variable lines with comments, unquoted spaces, unicode, multiline
    for i in range(300):
        lines.append(f"# Section comment header {i}")
        lines.append(f"UNQUOTED_VAR_{i}=value with unquoted spaces number {i} # trailing comment")
        lines.append(f"UNICODE_VAR_{i}=\"Unicode text こんにちは世界 🚀 {i}\"")
        lines.append(f"MULTILINE_VAR_{i}=\"line1\\nline2\\nline3 for item {i}\"")
        lines.append(f"EXPORT_VAR_{i}=simple_val_{i}")

    content = "\n".join(lines) + "\n"
    env_file.write_text(content, encoding="utf-8")
    example_file.write_text("EXPORT_VAR_0=simple_val_0\n", encoding="utf-8")

    doctor = EnvDoctor(str(env_file), str(example_file))

    start = time.perf_counter()
    vars_map, errors = doctor.parse_env_file(str(env_file))
    duration = time.perf_counter() - start

    assert errors == []
    assert len(vars_map) == 1200
    assert vars_map["UNQUOTED_VAR_10"] == "value with unquoted spaces number 10"
    assert vars_map["UNICODE_VAR_10"] == "Unicode text こんにちは世界 🚀 10"
    assert vars_map["MULTILINE_VAR_10"] == "line1\\nline2\\nline3 for item 10"
    assert vars_map["EXPORT_VAR_10"] == "simple_val_10"
    assert duration < 1.0

def test_benchmark_check_variables_large_comparison(tmp_path):
    """Verify check_variables performance with 1,000+ variable definitions in both files."""
    env_file = tmp_path / ".env"
    example_file = tmp_path / ".env.example"

    env_lines = []
    example_lines = []
    for i in range(1000):
        env_lines.append(f"CONFIG_PARAM_{i}=runtime_val_{i}")
        example_lines.append(f"CONFIG_PARAM_{i}=default_val_{i}")

    # Add 10 missing in env, 10 extra in env
    for i in range(1000, 1010):
        example_lines.append(f"MISSING_PARAM_{i}=default")
    for i in range(1010, 1020):
        env_lines.append(f"EXTRA_PARAM_{i}=value")

    env_file.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    example_file.write_text("\n".join(example_lines) + "\n", encoding="utf-8")

    doctor = EnvDoctor(str(env_file), str(example_file))

    start = time.perf_counter()
    res = doctor.check_variables()
    duration = time.perf_counter() - start

    assert len(res["missing_vars"]) == 10
    assert len(res["extra_vars"]) == 10
    assert len(res["env_vars"]) == 1010
    assert len(res["ex_vars"]) == 1010
    assert res["errors"] == []
    assert duration < 1.0
