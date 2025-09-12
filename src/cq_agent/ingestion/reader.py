from __future__ import annotations

import hashlib
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set, TypedDict, Tuple

from concurrent.futures import ThreadPoolExecutor, as_completed
import json


SUPPORTED_EXT_TO_LANG: Dict[str, str] = {
	".py": "python",
	".pyw": "python",
	".js": "javascript",
	".mjs": "javascript",
	".cjs": "javascript",
	".ts": "typescript",
	".tsx": "typescript",
}

IGNORED_DIR_NAMES: Set[str] = {
	".git",
	".hg",
	".svn",
	"node_modules",
	"dist",
	"build",
	"out",
	"__pycache__",
	".venv",
	"venv",
}

MAX_BYTES_PER_FILE_DEFAULT: int = 1_000_000  # 1 MB safety cap for MVP


class FileRecord(TypedDict):
	path: str
	language: Optional[str]
	text: str
	sloc: int
	hash: str


class GitStats(TypedDict):
	is_repo: bool
	churn_by_file: Dict[str, int]  # number of commits touching file
	last_modified_unix_by_file: Dict[str, int]


class RepoContext(TypedDict):
	root: str
	files: Dict[str, FileRecord]
	languages: List[str]
	git: GitStats
	summary: Dict[str, int]


def _is_git_repo(root: Path) -> bool:
	return (root / ".git").exists()


def _git_available() -> bool:
	try:
		result = subprocess.run(["git", "--version"], capture_output=True, text=True)
		return result.returncode == 0
	except Exception:
		return False


def _git_head(root: Path) -> str:
	if not _git_available() or not _is_git_repo(root):
		return "nogit"
	try:
		res = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(root), capture_output=True, text=True, timeout=5)
		if res.returncode == 0:
			return res.stdout.strip() or "nogit"
		return "nogit"
	except Exception:
		return "nogit"


def _git_file_churn(root: Path, rel_path: str) -> int:
	if not _git_available() or not _is_git_repo(root):
		return 0
	try:
		res = subprocess.run(
			["git", "log", "--follow", "--oneline", "--", rel_path],
			cwd=str(root), capture_output=True, text=True, timeout=10,
		)
		if res.returncode != 0:
			return 0
		return len([line for line in res.stdout.splitlines() if line.strip()])
	except Exception:
		return 0


def _git_last_modified_unix(root: Path, rel_path: str) -> int:
	if not _git_available() or not _is_git_repo(root):
		return 0
	try:
		res = subprocess.run(
			["git", "log", "-1", "--format=%ct", "--", rel_path],
			cwd=str(root), capture_output=True, text=True, timeout=5,
		)
		if res.returncode != 0:
			return 0
		value = res.stdout.strip()
		return int(value) if value.isdigit() else 0
	except Exception:
		return 0


def detect_language(path: str, first_line: Optional[str]) -> Optional[str]:
	ext = Path(path).suffix.lower()
	if ext_lang := SUPPORTED_EXT_TO_LANG.get(ext):
		return ext_lang
	if first_line and first_line.startswith("#!/"):
		line = first_line.lower()
		if "python" in line:
			return "python"
		if "node" in line or "deno" in line:
			return "javascript"
	return None


def _looks_binary(sample: bytes) -> bool:
	# Heuristic: presence of NUL byte or too many non-text bytes
	if b"\x00" in sample:
		return True
	# Allow common text whitespace and ascii range; count others
	text_chars = bytes({7, 8, 9, 10, 12, 13, 27} | set(range(32, 127)))
	nontext = sum(1 for b in sample if b not in text_chars)
	return nontext / max(1, len(sample)) > 0.30


def read_text(path: Path, max_bytes: int = MAX_BYTES_PER_FILE_DEFAULT) -> str:
	with path.open("rb") as f:
		sample = f.read(min(4096, max_bytes))
		if _looks_binary(sample):
			return ""
		# read rest if needed
		remaining = b""
		if len(sample) < max_bytes:
			remaining = f.read(max_bytes - len(sample))
		data = sample + remaining
	try:
		return data.decode("utf-8", errors="replace")
	except Exception:
		return ""


def _count_sloc(text: str) -> int:
	return sum(1 for line in text.splitlines() if line.strip())


def _sha256_text(text: str) -> str:
	return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _should_skip_dir(dir_name: str) -> bool:
	return dir_name in IGNORED_DIR_NAMES


def _git_check_ignore(root: Path, rel_path: str) -> bool:
	# Best-effort: rely on `git check-ignore` if available to honor .gitignore
	if not _git_available() or not _is_git_repo(root):
		return False
	try:
		res = subprocess.run(
			["git", "check-ignore", "-q", rel_path], cwd=str(root)
		)
		return res.returncode == 0
	except Exception:
		return False


def _load_repo_cache(cache_path: Path) -> Dict:
	if not cache_path.exists():
		return {}
	try:
		return json.load(cache_path.open("r", encoding="utf-8"))
	except Exception:
		return {}


def _save_repo_cache(cache_path: Path, data: Dict) -> None:
	try:
		cache_path.parent.mkdir(parents=True, exist_ok=True)
		json.dump(data, cache_path.open("w", encoding="utf-8"))
	except Exception:
		pass


def load_repo(path: str, max_files: int = 2000, max_bytes_per_file: int = MAX_BYTES_PER_FILE_DEFAULT, incremental: bool = True) -> RepoContext:
	root = Path(path).expanduser().resolve()
	if not root.exists():
		raise FileNotFoundError(f"Path not found: {root}")

	files: Dict[str, FileRecord] = {}
	languages: Set[str] = set()
	churn: Dict[str, int] = {}
	last_mod: Dict[str, int] = {}

	# Prepare cache
	repo_head = _git_head(root)
	cache_dir = Path.home() / ".cq_agent_cache"
	cache_path = cache_dir / f"repo_{hashlib.sha1((str(root)+repo_head).encode()).hexdigest()}.json"
	cache = _load_repo_cache(cache_path) if incremental else {}
	cached_files: Dict[str, Dict] = cache.get("files", {}) if isinstance(cache, dict) else {}
	cached_mtimes: Dict[str, float] = cache.get("mtimes", {}) if isinstance(cache, dict) else {}

	# First, collect candidate file paths sequentially (cheap)
	candidates: List[Path] = []
	candidate_stats: Dict[str, Tuple[float, int]] = {}
	for dirpath, dirnames, filenames in os.walk(root):
		# prune ignored dirs in-place
		dirnames[:] = [d for d in dirnames if not _should_skip_dir(d)]

		for filename in filenames:
			if len(candidates) >= max_files:
				break
			full_path = Path(dirpath) / filename
			rel_path = str(full_path.relative_to(root))

			# skip ignored by git
			if _git_check_ignore(root, rel_path):
				continue

			candidates.append(full_path)
			# lightweight fs stats for sampling (mtime, size)
			try:
				st = full_path.stat()
				candidate_stats[rel_path] = (float(st.st_mtime), int(st.st_size))
			except Exception:
				candidate_stats[rel_path] = (0.0, 0)

	# Pre-compute mtimes for incremental
	current_mtimes: Dict[str, float] = {}
	for p in candidates:
		try:
			current_mtimes[str(p.relative_to(root))] = p.stat().st_mtime
		except Exception:
			current_mtimes[str(p.relative_to(root))] = 0.0

	# Optional: deterministic sampling tiers
	def _select_sampling_tiers(paths: List[Path], limit: int) -> List[Path]:
		if limit <= 0 or len(paths) <= limit:
			return paths[:limit]
		# Ratios for core, recent, heavy
		core_quota = max(1, int(limit * 0.5))
		recent_quota = max(1, int(limit * 0.3))
		heavy_quota = max(1, limit - core_quota - recent_quota)

		def _rel(p: Path) -> str:
			return str(p.relative_to(root))

		def _core_score(rel: str) -> int:
			rel_l = rel.lower()
			score = 0
			for token in ("/src/", "\\src\\", "/app/", "\\app\\", "/lib/", "\\lib\\"):
				if token in rel_l:
					score += 3
			for token in ("core", "main", "service", "api", "model"):
				if token in rel_l:
					score += 1
			return score

		scored_core = sorted(paths, key=lambda p: (_core_score(_rel(p)), candidate_stats.get(_rel(p), (0.0, 0))[0]), reverse=True)
		scored_recent = sorted(paths, key=lambda p: candidate_stats.get(_rel(p), (0.0, 0))[0], reverse=True)
		scored_heavy = sorted(paths, key=lambda p: candidate_stats.get(_rel(p), (0.0, 0))[1], reverse=True)

		selected: List[Path] = []
		seen: Set[str] = set()

		def _take(from_list: List[Path], n: int):
			for p in from_list:
				rp = _rel(p)
				if rp in seen:
					continue
				selected.append(p)
				seen.add(rp)
				if len(selected) >= len(paths) or len(selected) >= limit:
					break

		_take(scored_core, core_quota)
		if len(selected) < limit:
			_take(scored_recent, recent_quota)
		if len(selected) < limit:
			_take(scored_heavy, heavy_quota)
		if len(selected) < limit:
			_take(scored_recent, limit - len(selected))
		return selected[:limit]

	# Decide unchanged vs changed
	unchanged_paths: Set[str] = set()
	changed_paths: List[Path] = []
	if incremental and cached_mtimes:
		for p in candidates:
			rel = str(p.relative_to(root))
			if rel in cached_mtimes and abs(cached_mtimes.get(rel, -1) - current_mtimes.get(rel, -2)) < 1e-6 and rel in cached_files:
				unchanged_paths.add(rel)
			else:
				changed_paths.append(p)
	else:
		changed_paths = candidates

	# Apply sampling tiers to bound heavy work
	if changed_paths and len(changed_paths) > 0:
		remaining_budget = max(0, max_files - len(files))
		if remaining_budget > 0:
			changed_paths = _select_sampling_tiers(changed_paths, remaining_budget)

	# Reuse cached FileRecords for unchanged
	for rel in unchanged_paths:
		rec = cached_files.get(rel)
		if not rec:
			continue
		files[rel] = FileRecord(
			path=rel,
			language=rec.get("language"),
			text=rec.get("text", ""),
			sloc=int(rec.get("sloc", 0)),
			hash=rec.get("hash", ""),
		)
		if rec.get("language"):
			languages.add(rec.get("language"))
		if len(files) >= max_files:
			changed_paths = []
			break

	# Worker to read file, detect language, compute metrics
	def _process_file(full_path: Path) -> Optional[FileRecord]:
		rel_path_inner = str(full_path.relative_to(root))
		# Consider only files likely to be code
		first_line: Optional[str] = None
		try:
			with full_path.open("rb") as fb:
				raw = fb.readline(256)
				try:
					first_line = raw.decode("utf-8", errors="ignore")
				except Exception:
					first_line = None
		except Exception:
			first_line = None

		language = detect_language(rel_path_inner, first_line)
		if language is None:
			return None

		text = read_text(full_path, max_bytes=max_bytes_per_file)
		if not text.strip():
			return None

		sloc = _count_sloc(text)
		digest = _sha256_text(text)
		return FileRecord(
			path=rel_path_inner,
			language=language,
			text=text,
			sloc=sloc,
			hash=digest,
		)

	# Parallel read/process changed files
	max_workers = min(32, (os.cpu_count() or 4) * 2)
	if changed_paths:
		with ThreadPoolExecutor(max_workers=max_workers) as executor:
			futures = [executor.submit(_process_file, p) for p in changed_paths]
			for fut in as_completed(futures):
				rec = fut.result()
				if rec is None:
					continue
				files[rec["path"]] = rec
				languages.add(rec["language"] or "")
				if len(files) >= max_files:
					break

	# git metadata (sequential; short timeouts inside helpers)
	for rel_path in list(files.keys()):
		churn[rel_path] = _git_file_churn(root, rel_path)
		last_mod[rel_path] = _git_last_modified_unix(root, rel_path)

	git_stats: GitStats = GitStats(
		is_repo=_is_git_repo(root),
		churn_by_file=churn,
		last_modified_unix_by_file=last_mod,
	)

	repo: RepoContext = RepoContext(
		root=str(root),
		files=files,
		languages=sorted([l for l in languages if l]),
		git=git_stats,
		summary={
			"file_count": len(files),
			"sloc_total": sum(f["sloc"] for f in files.values()),
		},
	)

	# Save cache for next run
	if incremental:
		cache_out = {
			"files": files,
			"mtimes": current_mtimes,
			"root": str(root),
			"head": repo_head,
		}
		_save_repo_cache(cache_path, cache_out)

	return repo
