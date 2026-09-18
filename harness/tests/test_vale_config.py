"""Regression tests for the repository's Vale prose configuration."""

from __future__ import annotations

import subprocess
from pathlib import Path

from harness.tests.conftest import REPO_ROOT


def test_vale_checks_comments_and_docstrings_but_not_string_literals(tmp_path: Path) -> None:
    """The Python View should lint prose nodes without treating normal strings as prose."""
    sample = tmp_path / "sample.py"
    sample.write_text(
        '"""We utilize a deliberately wordy verb in the module docstring."""\n'
        '\n'
        'class Example:\n'
        '    """We utilize another wordy verb in the class docstring."""\n'
        '\n'
        '    def method(self) -> str:\n'
        '        """We utilize the word again in the function docstring."""\n'
        '        return "utilize should stay ordinary code data"\n'
        '\n'
        '# In order to keep this comment clear, use the shorter phrase.\n',
        encoding="utf-8",
    )

    result = subprocess.run(
        ["vale", "--config", str(REPO_ROOT / ".vale.ini"), "--output=line", str(sample)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    output = result.stdout
    assert output.count("LoopGate.PlainWords") == 4
    assert "ordinary code data" not in output
    assert "sample.py:" in output
