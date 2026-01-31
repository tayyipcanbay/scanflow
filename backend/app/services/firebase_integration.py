"""
Firebase integration service for syncing FastAPI data to Firebase.
"""
import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    logging.warning("Firebase Admin SDK not installed. Firebase integration disabled.")

logger = logging.getLogger(__name__)


class FirebaseIntegration:
    """Service to sync FastAPI mesh data to Firebase Digital Twin."""
    
    def __init__(self):
        """Initialize Firebase connection."""
        self.db = None
        self._initialize_firebase()
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK."""
        if not FIREBASE_AVAILABLE:
            logger.warning("Firebase Admin SDK not available. Running in mock mode.")
            return
        
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Try to use service account key if available
                cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
                if cred_path and os.path.exists(cred_path):
                    cred = credentials.Certificate(cred_path)
                    firebase_admin.initialize_app(cred)
                else:
                    # Use default credentials (for emulator or GCP)
                    try:
                        firebase_admin.initialize_app()
                    except ValueError:
                        # Already initialized or no credentials
                        logger.info("Firebase already initialized or using emulator")
            
            self.db = firestore.client()
            logger.info("Firebase initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")
            self.db = None
    
    def sync_mesh_to_digital_twin(
        self,
        user_id: str,
        mesh_data: Dict[str, Any],
        comparison_data: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Sync mesh upload and comparison data to Firebase Digital Twin.
        
        Args:
            user_id: Firebase user UID
            mesh_data: Mesh upload information
            comparison_data: Optional comparison results
            
        Returns:
            True if sync successful, False otherwise
        """
        if not self.db:
            logger.warning("Firebase not available. Skipping sync.")
            return False
        
        try:
            user_ref = self.db.collection("users").document(user_id)
            twin_ref = user_ref.collection("digitalTwin").document("latest")
            
            # Extract metrics from mesh data
            digital_twin_data = {
                "timestamp": firestore.SERVER_TIMESTAMP,
                "scanUrl": mesh_data.get("file_path", ""),
                "weight": mesh_data.get("weight", 75.0),
                "bodyFat": mesh_data.get("body_fat", 18.5),
                "muscleMass": mesh_data.get("muscle_mass", 42.1),
                "bmi": mesh_data.get("bmi", 23.4),
                "bmrKcal": mesh_data.get("bmr", 1800),
            }
            
            # Add comparison data if available
            if comparison_data:
                stats = comparison_data.get("statistics", {})
                region_stats = comparison_data.get("region_statistics", {})
                
                digital_twin_data.update({
                    "lastComparison": {
                        "avgMagnitude": stats.get("avg_magnitude", 0.0),
                        "maxMagnitude": stats.get("max_magnitude", 0.0),
                        "increasePercentage": stats.get("increase_percentage", 0.0),
                        "decreasePercentage": stats.get("decrease_percentage", 0.0),
                    },
                    "regionChanges": region_stats,
                    "comparisonTimestamp": firestore.SERVER_TIMESTAMP
                })
            
            # Update Digital Twin
            twin_ref.set(digital_twin_data, merge=True)
            logger.info(f"Synced mesh data to Digital Twin for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to sync to Digital Twin: {e}")
            return False
    
    def trigger_ai_plan_regeneration(self, user_id: str) -> bool:
        """
        Trigger AI plan regeneration after mesh comparison.
        
        Args:
            user_id: Firebase user UID
            
        Returns:
            True if triggered successfully
        """
        if not self.db:
            logger.warning("Firebase not available. Skipping AI trigger.")
            return False
        
        try:
            # Update a flag that triggers plan regeneration
            user_ref = self.db.collection("users").document(user_id)
            user_ref.update({
                "planRegenerationRequested": True,
                "lastMeshUpdate": firestore.SERVER_TIMESTAMP
            })
            logger.info(f"Triggered AI plan regeneration for user {user_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to trigger AI regeneration: {e}")
            return False
    
    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile from Firebase.
        
        Args:
            user_id: Firebase user UID
            
        Returns:
            User profile data or None
        """
        if not self.db:
            return None
        
        try:
            user_ref = self.db.collection("users").document(user_id)
            doc = user_ref.get()
            if doc.exists:
                return doc.to_dict()
            return None
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return None


# Global instance
firebase_integration = FirebaseIntegration()

