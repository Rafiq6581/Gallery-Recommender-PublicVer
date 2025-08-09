from google.cloud import firestore
from loguru import logger
db = firestore.Client()

def save_report(uid: str, report: str):
    db.collection("exhibition_reports").document(uid).set({"report": report}    )


def delete_report(uid: str):
    try:
        doc_ref = db.collection("exhibition_reports").document(uid)
        doc_ref.delete()
        logger.info(f"Deleted cached report for {uid}")
    except Exception as e:
        logger.error(f"Failed to delete: {e}")

def fetch_report(uid: str):
    doc = db.collection("exhibition_reports").document(uid).get()
    if doc.exists:
        return doc.to_dict().get("report", None)
    else:
        return None
    
