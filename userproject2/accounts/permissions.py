from rest_framework import permissions
from datetime import date, datetime

class IsAdultUser(permissions.BasePermission):  # Custom permission to allow only adult users (18+) to access certain views
    message = "Access denied: you must be at least 18 years old."

    def has_permission(self, request, view):  # Check if user is adult
        user = request.user  # Get the user from request

        # 1️⃣ Ensure user is authenticated
        if not user or not user.is_authenticated:  # Check if user is authenticated
            self.message = "Authentication required."  # Update message for unauthenticated users
            return False  # Deny access if not authenticated

        # 2️⃣ Check if date_of_birth exists
        dob = getattr(user, "date_of_birth", None)  # Get date_of_birth attribute
        if not dob:
            self.message = "Date of birth not provided."
            return False

        # 3️⃣ Convert dob to date if string
        if isinstance(dob, str):  # If dob is string, convert to date
            dob = datetime.strptime(dob, "%Y-%m-%d").date()

        # 4️⃣ Calculate age
        today = date.today()  # Get today's date
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))  # Calculate age

        # 5️⃣ Deny access if under 18
        if age < 18:  # If user is under 18
            self.message = f"Access denied — you are only {age} years old."   # Deny access if under 18
            return False

        # ✅ User is adult
        return True  # Allow access if 18 or older
