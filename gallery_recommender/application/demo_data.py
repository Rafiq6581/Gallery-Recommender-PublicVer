"""
Demo data generator for Art Gallery Recommender
This module provides mock data for demonstration and testing purposes.
"""

import datetime
from typing import List, Dict, Any
from uuid import uuid4

def generate_demo_galleries() -> List[Dict[str, Any]]:
    """Generate demo gallery data for testing."""
    return [
        {
            "id": str(uuid4()),
            "name": "Downtown Modern Art Gallery",
            "name_japanese": "ダウンタウン近代美術館",
            "name_english": "Downtown Modern Art Gallery",
            "description": "A contemporary gallery featuring modern and digital art exhibitions.",
            "address_japanese": "東京都中央区銀座1-1-1",
            "address_english": "1-1-1 Ginza, Chuo-ku, Tokyo",
            "area": "DOWNTOWN",
            "gallery_image_url": "https://example.com/gallery1.jpg",
            "website": "https://example.com/gallery1",
            "hours": "10:00-18:00 (Closed Mondays)",
            "latitude": 35.6704,
            "longitude": 139.7704,
            "phone_number": "+81-3-1234-5678"
        },
        {
            "id": str(uuid4()),
            "name": "Waterfront Art Space",
            "name_japanese": "ウォーターフロントアートスペース",
            "name_english": "Waterfront Art Space",
            "description": "Scenic gallery overlooking the bay, specializing in landscape and environmental art.",
            "address_japanese": "東京都港区台場2-2-2",
            "address_english": "2-2-2 Daiba, Minato-ku, Tokyo",
            "area": "WATERFRONT",
            "gallery_image_url": "https://example.com/gallery2.jpg",
            "website": "https://example.com/gallery2",
            "hours": "11:00-19:00 (Closed Tuesdays)",
            "latitude": 35.6297,
            "longitude": 139.7756,
            "phone_number": "+81-3-2345-6789"
        },
        {
            "id": str(uuid4()),
            "name": "Cultural Heritage Gallery",
            "name_japanese": "文化遺産ギャラリー",
            "name_english": "Cultural Heritage Gallery",
            "description": "Traditional gallery showcasing classical and cultural artworks.",
            "address_japanese": "東京都台東区上野3-3-3",
            "address_english": "3-3-3 Ueno, Taito-ku, Tokyo",
            "area": "HISTORIC_DISTRICT",
            "gallery_image_url": "https://example.com/gallery3.jpg",
            "website": "https://example.com/gallery3",
            "hours": "9:00-17:00 (Closed Wednesdays)",
            "latitude": 35.7148,
            "longitude": 139.7753,
            "phone_number": "+81-3-3456-7890"
        }
    ]

def generate_demo_exhibitions() -> List[Dict[str, Any]]:
    """Generate demo exhibition data for testing."""
    galleries = generate_demo_galleries()
    
    exhibitions = []
    exhibition_data = [
        {
            "name": "Digital Dreams: Contemporary VR Art",
            "name_japanese": "デジタルドリーム：現代VRアート",
            "name_english": "Digital Dreams: Contemporary VR Art",
            "description": "An immersive exhibition exploring virtual reality as an artistic medium, featuring interactive installations and digital landscapes.",
            "description_japanese": "バーチャルリアリティを芸術媒体として探求する没入型展示。",
            "description_english": "An immersive exhibition exploring virtual reality as an artistic medium, featuring interactive installations and digital landscapes.",
            "artist": "Maya Chen & Digital Collective",
            "exhibition_image_url": "https://example.com/exhibition1.jpg",
            "gallery_id": galleries[0]["id"],
            "area": galleries[0]["area"]
        },
        {
            "name": "Ocean Waves: Marine Environment Photography",
            "name_japanese": "海の波：海洋環境写真",
            "name_english": "Ocean Waves: Marine Environment Photography",
            "description": "Stunning underwater and coastal photography capturing the beauty and fragility of marine ecosystems.",
            "description_japanese": "海洋生態系の美しさと脆弱性を捉えた見事な水中・沿岸写真。",
            "description_english": "Stunning underwater and coastal photography capturing the beauty and fragility of marine ecosystems.",
            "artist": "James Rivera",
            "exhibition_image_url": "https://example.com/exhibition2.jpg",
            "gallery_id": galleries[1]["id"],
            "area": galleries[1]["area"]
        },
        {
            "name": "Edo Period Masters: Classical Japanese Painting",
            "name_japanese": "江戸時代の巨匠：古典日本画",
            "name_english": "Edo Period Masters: Classical Japanese Painting",
            "description": "A retrospective of masterful works from the Edo period, showcasing traditional techniques and cultural themes.",
            "description_japanese": "江戸時代の傑作作品の回顧展。伝統技法と文化的テーマを紹介。",
            "description_english": "A retrospective of masterful works from the Edo period, showcasing traditional techniques and cultural themes.",
            "artist": "Historical Collection",
            "exhibition_image_url": "https://example.com/exhibition3.jpg",
            "gallery_id": galleries[2]["id"],
            "area": galleries[2]["area"]
        }
    ]
    
    for i, exhibition in enumerate(exhibition_data):
        start_date = datetime.datetime.now() + datetime.timedelta(days=i*30)
        end_date = start_date + datetime.timedelta(days=90)
        
        exhibition.update({
            "id": str(uuid4()),
            "exhibition_start_date": start_date,
            "exhibition_end_date": end_date,
            "exhibition_start_date_ts": start_date.timestamp(),
            "exhibition_end_date_ts": end_date.timestamp(),
            "latitude": galleries[i]["latitude"],
            "longitude": galleries[i]["longitude"]
        })
        exhibitions.append(exhibition)
    
    return exhibitions

def generate_demo_queries() -> List[Dict[str, Any]]:
    """Generate demo query examples for testing."""
    return [
        {
            "level": "beginner",
            "duration": "2 hours",
            "reason": "relaxation",
            "mood": "contemplative",
            "area": "DOWNTOWN"
        },
        {
            "level": "intermediate",
            "duration": "half day",
            "reason": "inspiration",
            "mood": "curious",
            "area": "WATERFRONT"
        },
        {
            "level": "expert",
            "duration": "full day",
            "reason": "education",
            "mood": "analytical",
            "area": "HISTORIC_DISTRICT"
        }
    ]

class DemoDataManager:
    """Manages demo data for the Art Gallery Recommender."""
    
    def __init__(self):
        self.galleries = generate_demo_galleries()
        self.exhibitions = generate_demo_exhibitions()
        self.queries = generate_demo_queries()
    
    def get_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get all demo data."""
        return {
            "galleries": self.galleries,
            "exhibitions": self.exhibitions,
            "queries": self.queries
        }
    
    def save_to_mongodb(self, db_connection):
        """Save demo data to MongoDB (if available)."""
        try:
            db_connection.galleries.insert_many(self.galleries)
            db_connection.exhibitions.insert_many(self.exhibitions)
            print("Demo data saved to MongoDB successfully.")
        except Exception as e:
            print(f"Could not save to MongoDB: {e}")
    
    def export_to_json(self, filepath: str):
        """Export demo data to JSON file."""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.get_all_data(), f, indent=2, default=str)
        print(f"Demo data exported to {filepath}")

if __name__ == "__main__":
    # Generate and export demo data
    demo_manager = DemoDataManager()
    demo_manager.export_to_json("demo_data.json")
    print("Demo data generated successfully!")
