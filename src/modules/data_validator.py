import re

class DataValidator:
    @staticmethod
    def validate_license_plate(plate):
        """Deterministic Guardrail for License Plates"""
        if not plate:
            return None
        # Allow alphanumeric, hyphens, and spaces.
        clean_plate = re.sub(r'[^A-Z0-9\-\s]', '', plate.upper()).strip()
        # Widen the length constraint to avoid rejecting foreign/special plates
        if len(clean_plate) >= 4 and len(clean_plate) <= 12:
            return clean_plate
        return "INVALID_FORMAT"

    @staticmethod
    def validate_date(date_str):
        """Deterministic Guardrail for Dates (Robust parsing, India default DD-MM-YYYY)"""
        if not date_str:
            return None
        
        try:
            from dateutil import parser
            # dayfirst=True ensures ambiguous dates (like 10/11/2023) are treated as DD/MM/YYYY (India Standard)
            parsed_date = parser.parse(date_str, fuzzy=True, dayfirst=True)
            # Standardize output format
            return parsed_date.strftime("%d-%m-%Y")
        except Exception:
            return "INVALID_FORMAT"
