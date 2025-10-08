from rest_framework import permissions
from datetime import date, datetime
from accounts.models import CustomUser

class IsAdultUser(permissions.BasePermission):
    message = "Access denied: you must be at least 18 years old."

    def has_permission(self, request, view):
        user = request.user

        # 1️⃣ Ensure the user is authenticated
        if not user or not user.is_authenticated:
            self.message = "Authentication required."
            return False

        # 2️⃣ Fetch fresh user record from DB
        try:
            db_user = CustomUser.objects.get(id=user.id)
        except CustomUser.DoesNotExist:
            self.message = "User not found."
            return False

        dob = db_user.date_of_birth

        # 3️⃣ Check if DOB exists
        if not dob:
            self.message = "Date of birth not provided."
            return False

        # 4️⃣ Ensure dob is a date object (sometimes it comes as string)
        if isinstance(dob, str):
            dob = datetime.strptime(dob, "%Y-%m-%d").date()

        # 5️⃣ Calculate accurate age
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # 6️⃣ Deny access if user < 18
        if age < 18:
            self.message = f"Access denied — you are only {age} years old."
            return False

        return True
