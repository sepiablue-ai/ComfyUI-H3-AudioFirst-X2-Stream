"""Installation must be repeatable and preserve differing installed files."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("audiofirst_setup_test", Path(__file__).resolve().parents[1] / "setup.py")
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


class SetupTests(unittest.TestCase):
    def test_repeated_install_and_conflict_preservation(self):
        scratch = setup.ROOT / "tmp"
        scratch.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="audiofirst_setup_", dir=scratch) as temporary:
            root = Path(temporary)
            target = setup.install_package(root)
            self.assertEqual(target, setup.install_package(root))
            self.assertTrue((target / "examples/fl2va_audiofirst_14s.json").is_file())
            existing = target / "README.md"
            existing.write_text("Keep the user's edited README", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                setup.install_package(root)
            self.assertEqual(existing.read_text(encoding="utf-8"), "Keep the user's edited README")

    def test_distribution_excludes_weights_results_media_and_git(self):
        files = setup.package_files()
        self.assertTrue(files)
        for path in files:
            self.assertFalse({".git", "__pycache__", "tmp", "results"}.intersection(path.relative_to(setup.ROOT).parts))
            self.assertNotIn(path.suffix, (".pyc", ".mp4", ".safetensors", ".pth"))


if __name__ == "__main__":
    unittest.main()
