"""One-off: inventory Python features in North s*/code.py. Not a lesson script."""

from __future__ import annotations

import collections
import re
from pathlib import Path

root = Path(r"d:\agent-learning\learn-claude-code-north")
files = sorted(root.glob("s*/code.py"))

patterns = {
    "__slots__": r"__slots__",
    "@property": r"@property",
    "@staticmethod": r"@staticmethod",
    "@classmethod": r"@classmethod",
    "@dataclass": r"@dataclass",
    "field(": r"\bfield\s*\(",
    "asdict": r"\basdict\b",
    "self.__priv": r"self\.__[a-zA-Z]",
    "self._priv": r"self\._[a-zA-Z]",
    "super()": r"super\s*\(",
    "async def": r"\basync\s+def\b",
    "await": r"\bawait\b",
    "threading": r"\bthreading\b",
    "Queue": r"\bQueue\b",
    "ThreadPool": r"ThreadPool|as_completed|concurrent",
    "yield": r"\byield\b",
    "contextmanager": r"contextmanager|ExitStack",
    "Enum": r"\bEnum\b",
    "ABC": r"\bABC\b|abstractmethod",
    "Protocol": r"\bProtocol\b",
    "TypedDict": r"\bTypedDict\b",
    "NamedTuple": r"\bNamedTuple\b",
    "Generic": r"\bGeneric\b",
    "Callable": r"\bCallable\b",
    "Optional": r"\bOptional\b",
    "Literal": r"\bLiteral\b",
    "match-case": r"^\s*match\s+",
    "walrus": r":=",
    "re module": r"^import re\b|\bre\.(compile|search|match|sub|findall)",
    "pathlib Path": r"\bPath\b",
    "json": r"\bjson\.",
    "subprocess": r"\bsubprocess\b",
    "copy": r"\bcopy\.(deepcopy|copy)",
    "functools": r"\bfunctools\b|\bpartial\b|\bwraps\b",
    "itertools": r"\bitertools\b",
    "datetime": r"\bdatetime\b|\btimedelta\b",
    "uuid": r"\buuid\b",
    "base64": r"\bbase64\b",
    "shutil": r"\bshutil\b",
    "glob/fnmatch": r"\bglob\b|\bfnmatch\b",
    "__repr__/__str__": r"__repr__|__str__",
    "__call__": r"__call__",
    "__enter__/__exit__": r"__enter__|__exit__",
    "getattr family": r"\b(getattr|setattr|hasattr|delattr)\b",
    "lambda": r"\blambda\b",
    "listcomp": r"\[.+\sfor\s",
    "dictcomp": r"\{[^}]*for\s",
    "any/all": r"\b(any|all)\s*\(",
    "map/filter": r"\b(map|filter)\s*\(",
    "enumerate": r"\benumerate\b",
    "zip": r"\bzip\s*\(",
    "sorted": r"\bsorted\s*\(",
    "isinstance": r"\bisinstance\b",
    "raise": r"\braise\b",
    "with": r"\bwith\b",
    "try": r"\btry:",
}

hits: dict[str, list[str]] = collections.defaultdict(list)
imports: collections.Counter[str] = collections.Counter()
decorators: collections.Counter[str] = collections.Counter()
classes: list[str] = []

for f in files:
    text = f.read_text(encoding="utf-8")
    session = f.parent.name
    for name, pat in patterns.items():
        if re.search(pat, text, re.M):
            hits[name].append(session)
    for m in re.finditer(r"^(?:from\s+(\S+)\s+import|import\s+(\S+))", text, re.M):
        mod = (m.group(1) or m.group(2)).split(".")[0].split(",")[0]
        imports[mod] += 1
    for m in re.finditer(r"^@(\w+)", text, re.M):
        decorators[m.group(1)] += 1
    for m in re.finditer(r"^class\s+(\w+)", text, re.M):
        classes.append(f"{session}.{m.group(1)}")

out = Path(r"d:\agent-learning\playground\python\_tmp_north_py.txt")
lines = ["=== FILES ===", str(len(files)), "", "=== DECORATORS ==="]
for k, v in decorators.most_common():
    lines.append(f"{k}: {v}")
lines += ["", "=== CLASSES ==="] + classes
lines += ["", "=== IMPORTS ==="]
for k, v in imports.most_common():
    lines.append(f"{k}: {v}")
lines += ["", "=== FEATURE HITS ==="]
for name, sess in sorted(hits.items(), key=lambda x: -len(x[1])):
    uniq = sorted(set(sess))
    lines.append(f"{name:22} n={len(uniq):2}  {', '.join(uniq)}")
out.write_text("\n".join(lines), encoding="utf-8")
print("wrote", out)
