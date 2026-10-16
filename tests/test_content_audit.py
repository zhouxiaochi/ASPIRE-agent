from pathlib import Path
import re

ROOT = Path(__file__).parents[1]
TEXT_SUFFIXES = {".py", ".md", ".toml", ".json", ".txt", ".gitignore"}

def tracked_text_files():
    for path in ROOT.rglob("*"):
        if path.is_file() and not any(part.startswith(".") and part not in {".gitignore"} for part in path.relative_to(ROOT).parts):
            if path.suffix in TEXT_SUFFIXES or path.name == ".gitignore": yield path

def test_no_cjk_characters_or_private_artifacts():
    cjk = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
    forbidden_names = {".bkp", ".apw", ".his", ".rep", ".pdf", ".png", ".jpg", ".jpeg"}
    for path in ROOT.rglob("*"):
        if path.is_file(): assert path.suffix.lower() not in forbidden_names
    for path in tracked_text_files(): assert not cjk.search(path.read_text(encoding="utf-8")), path

def test_public_naming_and_module_sizes():
    old_agent = "slim" + "-own-agent"
    old_role = "valid" + "ator"
    old_activity = "valid" + "ation"
    legacy_identifier = "asi" + "pre"
    for path in tracked_text_files():
        relative_path = path.relative_to(ROOT).as_posix().lower()
        text = path.read_text(encoding="utf-8").lower()
        assert legacy_identifier not in relative_path, path
        assert legacy_identifier not in text, path
        assert old_agent not in text, path
        assert old_role not in text, path
        assert old_activity not in text, path
    for path in (ROOT / "src").rglob("*.py"): assert len(path.read_text(encoding="utf-8").splitlines()) <= 300, path

def test_prompt_and_skill_domain_boundary():
    process_words = ["react" + "or", "col" + "umn", "separ" + "ator"]
    study_words = ["design" + " spec", "sensitiv" + "ity", "optim" + "ization", "recy" + "cle"]
    roots = [ROOT / "skills", ROOT / "src" / "aspire_agent" / "resources"]
    for root in roots:
        for path in root.rglob("*.md"):
            text = path.read_text(encoding="utf-8").lower()
            assert not any(word in text for word in process_words + study_words), path

def test_examples_are_templates_only():
    for path in (ROOT / "examples").glob("*"):
        text = path.read_text(encoding="utf-8").lower(); assert "describe the desired" in text; assert "answer" not in text
