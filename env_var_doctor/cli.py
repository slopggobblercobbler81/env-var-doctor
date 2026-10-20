import argparse
import sys
from .env_var_doctor import EnvDoctor

def main():
    parser = argparse.ArgumentParser(description="env-var-doctor: Validate and analyze .env files.")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    parser.add_argument("--example", default=".env.example", help="Path to .env.example file")
    parser.add_argument("--strict", action="store_true", help="Treat extra variables or warnings as errors")
    parser.add_argument("--check", action="store_true", help="Run check and exit with non-zero status on failure")

    args = parser.parse_args()

    doctor = EnvDoctor(env_path=args.env, example_path=args.example)
    results = doctor.check_variables()

    has_issues = False

    if results["errors"]:
        has_issues = True
        print("Syntax/Parsing Errors:")
        for err in results["errors"]:
            print(f"  - {err}")

    if results["missing_vars"]:
        has_issues = True
        print("Missing Variables (present in example, missing in env):")
        for var in results["missing_vars"]:
            print(f"  - {var}")

    if results["extra_vars"]:
        print("Extra Variables (present in env, missing in example):")
        for var in results["extra_vars"]:
            print(f"  - {var}")
        if args.strict:
            has_issues = True

    if not has_issues and not results["missing_vars"] and not results["extra_vars"] and not results["errors"]:
        print("All environment variables check out successfully!")

    if args.check and has_issues:
        sys.exit(1)

if __name__ == "__main__":
    main()
