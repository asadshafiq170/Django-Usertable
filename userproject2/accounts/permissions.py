from rest_framework import permissions
from datetime import date, datetime

class IsAdultUser(permissions.BasePermission):
    message = "Access denied: you must be at least 18 years old."

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            self.message = "Authentication required."
            return False

        dob = getattr(user, "date_of_birth", None)
        if not dob:
            self.message = "Date of birth not provided."
            return False

        if isinstance(dob, str):
            dob = datetime.strptime(dob, "%Y-%m-%d").date()

        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            self.message = f"Access denied — you are only {age} years old."
            return False
        return True
