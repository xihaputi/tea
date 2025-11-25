from pathlib import Path


class DiseaseModel:
    """Placeholder disease detection model."""

    def predict(self, image_path: Path) -> dict:
        # TODO: replace with real model inference
        return {
            "disease_type": "leaf_blur_mock",
            "confidence": 0.42,
            "advice": "Sample result: inspect leaves for pests and consider mild treatment.",
        }

