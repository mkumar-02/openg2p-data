"""Generate users/users.json from a subset of household heads."""

import json
import random
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEMO_DIR = REPO_ROOT / "demography"
OUT_DIR = REPO_ROOT / "users"

NUM_USERS = 20
SEED = 7
random.seed(SEED)

DP_ROLES_POOL = [
    "DP_region_kilima",
    "DP_region_faraja",
    "DP_region_jasiri",
    "DP_region_chakula",
]

ROLE_POOL = ["registry_user", "registry_admin", "registry_approver"]


def username_from(first: str, last: str, idx: int) -> str:
    base = (first[:1] + last).lower()
    base = "".join(c for c in base if c.isalnum()) or f"user{idx}"
    return base


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    households = json.loads((DEMO_DIR / "households.json").read_text())
    individuals_by_id = {
        i["internal_record_id"]: i
        for i in json.loads((DEMO_DIR / "individuals.json").read_text())
    }

    heads = [individuals_by_id[h["head_individual_id"]] for h in households]
    heads = heads[:NUM_USERS]

    users = []
    used_usernames: set[str] = set()
    for idx, ind in enumerate(heads, start=1):
        uname = username_from(ind["first_name"], ind["last_name"], idx)
        suffix = 0
        while uname in used_usernames:
            suffix += 1
            uname = f"{uname}{suffix}"
        used_usernames.add(uname)

        roles = ["registry_user"]
        if idx <= 3:
            roles.append("registry_admin")
        elif idx <= 6:
            roles.append("registry_approver")

        dp_roles = random.sample(DP_ROLES_POOL, k=random.randint(1, 3))

        users.append(
            {
                "username": uname,
                "email": ind["emails"] or f"{uname}@example.org",
                "first_name": ind["first_name"],
                "last_name": ind["last_name"],
                "individual_id": ind["internal_record_id"],
                "foundational_id": ind["foundational_id"],
                "roles": roles,
                "dp_roles": dp_roles,
            }
        )

    (OUT_DIR / "users.json").write_text(json.dumps(users, indent=2) + "\n")
    print(f"Wrote users.json: {len(users)} users")


if __name__ == "__main__":
    main()
