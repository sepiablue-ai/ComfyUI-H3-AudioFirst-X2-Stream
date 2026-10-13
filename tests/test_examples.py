"""The shipped API examples must keep the validated audio-first settings and complete connections."""
import json
from pathlib import Path
import unittest

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
FRAMES = {"05s": 124, "10s": 243, "14s": 345}


class ExampleTests(unittest.TestCase):
    def load(self, tag):
        return json.loads((EXAMPLES / "api" / f"fl2va_audiofirst_{tag}.api.json").read_text(encoding="utf-8"))

    def test_validated_settings(self):
        for tag, frames in FRAMES.items():
            graph = self.load(tag)
            self.assertEqual(graph["131"]["inputs"]["length"], frames)
            self.assertEqual(graph["201"]["inputs"]["length"], frames)
            self.assertEqual(graph["203"]["inputs"]["steps"], 6)
            self.assertEqual(graph["124"]["inputs"]["steps"], 4)
            self.assertEqual(graph["900"]["inputs"]["selection.keep_percent"], 5.0)
            self.assertEqual(graph["129"]["inputs"]["noise_seed"], 43)
            self.assertEqual(graph["125"]["inputs"]["latent_image"], ["206", 0])
            self.assertEqual(graph["92"]["inputs"]["audio"], ["121", 0])
            self.assertEqual(graph["121"]["inputs"]["samples"], ["205", 0])

    def test_connections_and_gui_copies(self):
        for tag in FRAMES:
            graph = self.load(tag)
            for key, node in graph.items():
                for value in node["inputs"].values():
                    if isinstance(value, list):
                        self.assertIn(value[0], graph, f"{tag}:{key}")
            gui = json.loads((EXAMPLES / f"fl2va_audiofirst_{tag}.json").read_text(encoding="utf-8"))
            self.assertEqual(sorted(str(node["id"]) for node in gui["nodes"]), sorted(graph))


if __name__ == "__main__":
    unittest.main()
